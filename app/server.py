import time
from config import Config
from app.utils.logger import log
from app.api.user import user_router
from app.job.cron_job import cron_job
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.schema.base_schema import BaseResponse
from app.middleware.usage import usage_middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError



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
    await cron_job()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=Config.app_name,
        description=Config.description,
        version="1.0.0",
        middleware=make_middleware(),
        lifespan=lifespan,
    )
    init_routers(app_=app_)
    return app_


app = create_app()


# Define a custom error handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Customize the response structure to be a single string
    response_content = BaseResponse(
        resp_code=422,
        response="\n".join(
            [
                f"Field '{'.'.join(map(str, error['loc']))}' - {error['msg']}"
                for error in exc.errors()
            ]
        )
    )
    return JSONResponse(
        status_code=422,
        content=response_content.model_dump()
    )


# Custom handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Format the response structure
    response_content = BaseResponse(
        resp_code=exc.detail.resp_code if isinstance(exc.detail, BaseResponse) else str(exc.status_code),
        response=exc.detail.response if isinstance(exc.detail, BaseResponse) else str(exc.detail)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response_content.model_dump()
    )


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