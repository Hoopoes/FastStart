from config import CONFIG
from fastapi import FastAPI
from app.jobs.cron_job import cron_job
from app.routes.route import API_ROUTER
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.errors.error_docs import GLOBAL_RESPONSES
from app.middleware.handler import register_middlewares
from app.core.exception_handler import register_error_handlers




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
    await cron_job()
    yield


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
    register_error_handlers(app=app_)
    register_middlewares(app=app_)
    return app_


app = create_app()