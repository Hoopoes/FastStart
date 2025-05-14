from fastapi import FastAPI
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


from config import CONFIG
from app.routes.route import API_ROUTER
from app.db.database import init_db, close_db
from app.errors.error_docs import GLOBAL_RESPONSES
from app.middlewares.exception import exception_handler
from app.middlewares.middleware import middleware_handler


def init_routers(app_: FastAPI) -> None:
    app_.include_router(API_ROUTER)


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run *before* the application starts (e.g., initialize DB, start background tasks)
    await init_db()
    yield
    # Code to run *after* the application shuts down (e.g., cleanup, close connections)
    await close_db()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=CONFIG.app_name,
        description=CONFIG.description,
        version=CONFIG.version,
        middleware=make_middleware(),
        lifespan=lifespan,
        responses=GLOBAL_RESPONSES,
        root_path=CONFIG.root_path,
        docs_url="/docs",
        redoc_url="/redoc",
        
    )
    init_routers(app_=app_)
    exception_handler(app=app_)
    middleware_handler(app=app_)
    return app_


app = create_app()