use crate::{
    database::{
        context::{
            get_session_database, get_sql_connect, insert_sql_session, remove_sql_session,
            set_sql_connect,
        },
        sql::{config::DatabaseConfig, connection::DatabaseConnection},
    },
    di::DependencyInjection,
    executor::{execute_http_function, execute_middleware_function, execute_startup_handler},
    instants::TokioExecutor,
    middlewares::base::{Middleware, MiddlewareConfig}, 
    router::router::Router,
    types::{
        body::{full, BoxBody},
        function_info::FunctionInfo,
        middleware::MiddlewareReturn,
        request::Request,
    },
    ws::{router::WebsocketRouter, socket::SocketHeld, websocket::websocket_handler},
};
use dashmap::DashMap;
use futures::future::join_all;
use hyper::{
    body::Incoming,
    server::conn::{http1, http2},
    service::service_fn,
    Request as HyperRequest, StatusCode,
};
use hyper::{header::HeaderValue, Response as HyperResponse};
use hyper_util::rt::TokioIo;
use pyo3::{prelude::*, types::PyDict};
use pyo3_asyncio::TaskLocals;
use std::{
    collections::HashMap,
    sync::{
        atomic::Ordering::{Relaxed, SeqCst},
        RwLock,
    },
    thread,
    time::{Duration, Instant},
};
use std::{
    process::exit,
    sync::{atomic::AtomicBool, Arc},
};

use tracing::{debug, info};
use tracing_subscriber::{fmt, layer::SubscriberExt, util::SubscriberInitExt};

static STARTED: AtomicBool = AtomicBool::new(false);
static NOTFOUND: &[u8] = b"Not Found";

struct SharedContext {
    router: Arc<RwLock<Router>>,
    ws_router: Arc<WebsocketRouter>,
    task_locals: Arc<TaskLocals>,
    middlewares: Arc<Middleware>,
    extra_headers: Arc<DashMap<String, String>>,
    dependencies: Arc<DependencyInjection>,
    http2: bool,
}

impl SharedContext {
    fn new(
        router: Arc<RwLock<Router>>,
        ws_router: Arc<WebsocketRouter>,
        task_locals: Arc<TaskLocals>,
        middlewares: Arc<Middleware>,
        extra_headers: Arc<DashMap<String, String>>,
        dependencies: Arc<DependencyInjection>,
        http2: bool,
    ) -> Self {
        Self {
            router,
            ws_router,
            task_locals,
            middlewares,
            extra_headers,
            dependencies,
            http2,
        }
    }

    fn clone(&self) -> Self {
        Self {
            router: Arc::clone(&self.router),
            ws_router: Arc::clone(&self.ws_router),
            task_locals: Arc::clone(&self.task_locals),
            middlewares: Arc::clone(&self.middlewares),
            extra_headers: Arc::clone(&self.extra_headers),
            dependencies: Arc::clone(&self.dependencies),
            http2: self.http2,
        }
    }
}

#[pyclass]
pub struct Server {
    router: Arc<RwLock<Router>>,
    websocket_router: Arc<WebsocketRouter>,
    startup_handler: Option<Arc<FunctionInfo>>,
    shutdown_handler: Option<Arc<FunctionInfo>>,
    middlewares: Arc<Middleware>,
    extra_headers: Arc<DashMap<String, String>>,
    database_config: Option<DatabaseConfig>,
    dependencies: Arc<DependencyInjection>,
    http2: bool,
}

#[pymethods]
impl Server {
    #[new]
    pub fn new() -> Self {
        Self {
            router: Arc::new(RwLock::new(Router::default())),
            websocket_router: Arc::new(WebsocketRouter::default()),
            startup_handler: None,
            shutdown_handler: None,
            middlewares: Arc::new(Middleware::new()),
            extra_headers: Arc::new(DashMap::new()),
            database_config: None,
            dependencies: Arc::new(DependencyInjection::default()),
            http2: false,
        }
    }

    pub fn inject(&mut self, key: &str, value: Py<PyAny>) {
        let _ = self.dependencies.add_dependency(key, value);
    }

    pub fn set_dependencies(&mut self, dependencies: Py<PyDict>) {
        self.dependencies = Arc::new(DependencyInjection::from_object(dependencies));
    }

    pub fn set_router(&mut self, router: Router) {
        // Update router
        self.router = Arc::new(RwLock::new(router));
    }

    pub fn set_websocket_router(&mut self, websocket_router: WebsocketRouter) {
        self.websocket_router = Arc::new(websocket_router);
    }

    pub fn set_before_hooks(&mut self, hooks: Vec<(FunctionInfo, MiddlewareConfig)>) {
        Arc::get_mut(&mut self.middlewares)
            .unwrap()
            .set_before_hooks(hooks);
    }

    pub fn set_after_hooks(&mut self, hooks: Vec<(FunctionInfo, MiddlewareConfig)>) {
        Arc::get_mut(&mut self.middlewares)
            .unwrap()
            .set_after_hooks(hooks);
    }

    pub fn set_response_headers(&mut self, headers: HashMap<String, String>) {
        for (key, value) in headers {
            self.extra_headers.insert(key, value);
        }
    }

    pub fn set_startup_handler(&mut self, handler: FunctionInfo) {
        self.startup_handler = Some(Arc::new(handler));
    }

    pub fn set_shutdown_handler(&mut self, handler: FunctionInfo) {
        self.shutdown_handler = Some(Arc::new(handler));
    }

    pub fn set_database_config(&mut self, config: DatabaseConfig) {
        self.database_config = Some(config);
    }

    pub fn enable_http2(&mut self) {
        self.http2 = true;
    }

    pub fn start(
        &mut self,
        py: Python,
        socket: &PyCell<SocketHeld>,
        workers: usize,
        max_blocking_threads: usize,
    ) -> PyResult<()> {
        tracing_subscriber::registry()
            .with(
                tracing_subscriber::EnvFilter::try_from_default_env()
                    .unwrap_or_else(|_| "debug".into()),
            )
            .with(
                fmt::layer()
                    .with_target(false)
                    .with_level(true)
                    .with_file(true),
            )
            .init();

        if STARTED
            .compare_exchange(false, true, SeqCst, Relaxed)
            .is_err()
        {
            return Ok(());
        }

        let raw_socket = socket.try_borrow_mut()?.get_socket();
        let asyncio = py.import("asyncio")?;
        let event_loop = asyncio.call_method0("get_event_loop")?;

        let _websocket_router = Arc::clone(&self.websocket_router);

        let startup_handler = self.startup_handler.clone();
        let shutdown_handler = self.shutdown_handler.clone();

        let task_locals = Arc::new(pyo3_asyncio::TaskLocals::new(event_loop).copy_context(py)?);
        let task_local_copy = Arc::clone(&task_locals);

        let database_config: Option<DatabaseConfig> = self.database_config.clone();

        let shared_context = SharedContext::new(
            self.router.clone(),
            self.websocket_router.clone(),
            task_locals.clone(),
            self.middlewares.clone(),
            self.extra_headers.clone(),
            self.dependencies.clone(),
            self.http2,
        );

        thread::spawn(move || {
            let rt = tokio::runtime::Builder::new_multi_thread()
                .worker_threads(workers)
                .max_blocking_threads(max_blocking_threads)
                .thread_keep_alive(Duration::from_secs(60))
                .thread_name("hypern-worker")
                .thread_stack_size(3 * 1024 * 1024) // 3MB stack
                .enable_all()
                .build()
                .unwrap();
            debug!(
                "Server start with {} workers and {} max blockingthreads",
                workers, max_blocking_threads
            );
            debug!("Waiting for process to start...");

            rt.block_on(async move {
                // excute startup handler
                let _ = execute_startup_handler(startup_handler, &Arc::clone(&task_locals)).await;

                let listener = tokio::net::TcpListener::from_std(raw_socket.into()).unwrap();

                match database_config {
                    Some(config) => {
                        let database = DatabaseConnection::new(config).await;
                        set_sql_connect(database);
                    }
                    None => {}
                };

                loop {
                    let (stream, _) = listener.accept().await.unwrap();
                    let io = TokioIo::new(stream);
                    let shared_context = shared_context.clone();
                    tokio::task::spawn(async move {
                        let svc = service_fn(|req: hyper::Request<hyper::body::Incoming>| {
                            let shared_context = shared_context.clone();
                            async move {
                                if hyper_tungstenite::is_upgrade_request(&req) {
                                    let response =
                                        websocket_service(req, shared_context.ws_router).await;
                                    return Ok::<_, hyper::Error>(response);
                                }
                                let response = http_service(req, shared_context).await;
                                Ok::<_, hyper::Error>(response)
                            }
                        });

                        match shared_context.http2 {
                            true => {
                                if let Err(err) = http2::Builder::new(TokioExecutor)
                                    .keep_alive_timeout(Duration::from_secs(60))
                                    .serve_connection(io, svc)
                                    .await
                                {
                                    debug!("Failed to serve connection: {:?}", err);
                                }
                            }
                            false => {
                                if let Err(err) = http1::Builder::new()
                                    .keep_alive(true)
                                    .serve_connection(io, svc)
                                    .with_upgrades()
                                    .await
                                {
                                    debug!("Failed to serve connection: {:?}", err);
                                }
                            }
                        }
                    });
                }
            });
        });

        let event_loop = (*event_loop).call_method0("run_forever");
        if event_loop.is_err() {
            if let Some(function) = shutdown_handler {
                if function.is_async {
                    pyo3_asyncio::tokio::run_until_complete(
                        task_local_copy.event_loop(py),
                        pyo3_asyncio::into_future_with_locals(
                            &task_local_copy.clone(),
                            function.handler.as_ref(py).call0()?,
                        )
                        .unwrap(),
                    )
                    .unwrap();
                } else {
                    Python::with_gil(|py| function.handler.call0(py))?;
                }
            }

            exit(0);
        }
        Ok(())
    }
}

async fn http_service(
    req: HyperRequest<Incoming>,
    shared_context: SharedContext,
) -> HyperResponse<BoxBody> {
    let path = req.uri().path().to_string();
    let method = req.method().to_string();
    let version = req.version();
    let user_agent = req
        .headers()
        .get("user-agent")
        .cloned()
        .unwrap_or(HeaderValue::from_str("unknown").unwrap());
    let start_time = Instant::now();

    // matching mapping router
    let route = {
        let router = shared_context.router.read().unwrap();
        router.find_matching_route(&path, &method)
    };

    let response = match route {
        Some((route, path_params)) => {
            let function = route.function;
            let mut request = Request::from_request(req).await;
            request.path_params = path_params;
            let response = mapping_method(
                request,
                function,
                shared_context.task_locals,
                shared_context.middlewares,
                shared_context.extra_headers,
                shared_context.dependencies,
            )
            .await;
            response
        }
        None => HyperResponse::builder()
            .status(StatusCode::NOT_FOUND)
            .body(full(NOTFOUND))
            .unwrap(),
    };
    // logging
    info!(
        "{:?} {:?} {:?} {:?} {:?} {:?}",
        version,
        method,
        path,
        user_agent,
        start_time.elapsed(),
        response.status(),
    );

    return response;
}

async fn websocket_service(
    req: HyperRequest<Incoming>,
    websocket_router: Arc<WebsocketRouter>,
) -> HyperResponse<BoxBody> {
    let path = req.uri().path().to_string();
    let route = websocket_router.find_route(&path);

    let response = match route {
        Some(route) => {
            let handler = route.handler.clone();
            let response = websocket_handler(handler, req).await;
            response.unwrap()
        }
        None => HyperResponse::new(full("Not a websocket request")),
    };
    return response;
}

async fn inject_database(request_id: Arc<String>) {
    let database = get_sql_connect();
    match database {
        Some(database) => {
            insert_sql_session(&request_id, database.transaction().await);
        }
        None => {}
    }
}

fn free_database(request_id: String) {
    tokio::task::spawn(async move {
        let tx = get_session_database(&request_id);
        match tx {
            None => return,
            Some(mut tx) => {
                tx.commit_internal().await;
                remove_sql_session(&request_id);
            }
        }
    });
}

async fn execute_request(
    mut request: Request,
    function: FunctionInfo,
    middlewares: Arc<Middleware>,
    extra_headers: Arc<DashMap<String, String>>,
    dependencies: Arc<DependencyInjection>,
) -> HyperResponse<BoxBody> {

    let response_builder = HyperResponse::builder();
    let request_id = Arc::new(request.context_id.clone());

    inject_database(Arc::clone(&request_id)).await;

    // Execute before middlewares in parallel where possible
    let before_results = join_all(
        middlewares
            .get_before_hooks()
            .into_iter()
            .filter(|(_, config)| !config.is_conditional)
            .map(|(middleware, _)| {
                let request = request.clone();
                let middleware = middleware.clone();
                async move { execute_middleware_function(&request, &middleware).await }
            }),
    )
    .await;

    // Process results and handle any errors
    for result in before_results {
        match result {
            Ok(MiddlewareReturn::Request(r)) => request = r,
            Ok(MiddlewareReturn::Response(r)) => return r.to_response(&extra_headers),
            Err(e) => {
                return response_builder
                    .body(full(format!("Error: {}", e)))
                    .unwrap();
            }
        }
    }

    // Execute conditional middlewares sequentially
    for (middleware, config) in middlewares.get_before_hooks() {
        if config.is_conditional {
            match execute_middleware_function(&request, &middleware).await {
                Ok(MiddlewareReturn::Request(r)) => request = r,
                Ok(MiddlewareReturn::Response(r)) => return r.to_response(&extra_headers),
                Err(e) => {
                    return HyperResponse::builder()
                        .status(StatusCode::INTERNAL_SERVER_ERROR)
                        .body(full(format!("Error: {}", e)))
                        .unwrap();
                }
            }
        }
    }

    // Execute the main handler
    let mut response = execute_http_function(&request, &function, Some(dependencies))
        .await
        .unwrap();

    // mapping context id
    response.context_id = request.context_id;

    // Execute after middlewares with similar optimization
    for (after_middleware, _) in middlewares.get_after_hooks() {
        response = match execute_middleware_function(&response, &after_middleware).await {
            Ok(MiddlewareReturn::Request(_)) => {
                return response_builder
                    .status(StatusCode::INTERNAL_SERVER_ERROR)
                    .body(full("Middleware returned a response"))
                    .unwrap();
            }
            Ok(MiddlewareReturn::Response(r)) => {
                let response = r;
                response
            }
            Err(e) => {
                return response_builder
                    .status(StatusCode::INTERNAL_SERVER_ERROR)
                    .body(full(e.to_string()))
                    .unwrap();
            }
        };
    }

    free_database(request_id.to_string());

    response.to_response(&extra_headers)
}

async fn mapping_method(
    req: Request,
    function: FunctionInfo,
    task_locals: Arc<pyo3_asyncio::TaskLocals>,
    middlewares: Arc<Middleware>,
    extra_headers: Arc<DashMap<String, String>>,
    dependencies: Arc<DependencyInjection>,
) -> HyperResponse<BoxBody> {
    pyo3_asyncio::tokio::scope(
        task_locals.as_ref().to_owned(),
        execute_request(req, function, middlewares, extra_headers, dependencies),
    )
    .await
}
