import time
from config import CONFIG
from app.utils.logger import log
from fastapi import FastAPI, Request
from app.api.user import user_router
from app.job.cron_job import cron_job
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager
from app.middleware.usage import usage_middleware
from fastapi.middleware.cors import CORSMiddleware
from app.schema.base_schema import GLOBAL_RESPONSES
from app.res.exception_handlers import register_error_handlers
from app.db.prisma_client import connect_prisma, disconnect_prisma


def init_routers(app_: FastAPI) -> None:
    app_.include_router(user_router)


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
    await connect_prisma()
    await cron_job()
    yield
    await disconnect_prisma()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=CONFIG.app_name,
        description=CONFIG.description,
        version="1.0.0",
        middleware=make_middleware(),
        lifespan=lifespan,
        responses=GLOBAL_RESPONSES
    )
    init_routers(app_=app_)
    register_error_handlers(app=app_)
    return app_


app = create_app()


@app.middleware("http")
async def outgoing_middleware(request: Request, call_next):
    start_time = time.monotonic()
    response = await call_next(request)
    
    # api_type = request.scope.get("type", "Unknown")
    route = request.scope.get("path", "Unknown")
    http_method = request.method

    response = await usage_middleware(response=response)

    process_time = time.monotonic() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    log.info(f"- {http_method} \"{route}\" Time Taken: {process_time:.2f} s 🚀")
    
    return response