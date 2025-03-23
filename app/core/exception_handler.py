from app.core.logger import LOG
from fastapi.responses import JSONResponse
from app.schema.base import BaseResponseDto
from app.res.error import InternalServerError
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


def register_error_handlers(app: FastAPI):
    # Validation error handler
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        response_content = BaseResponseDto(
            code="REQ_VALIDATION_FAILED",
            message="\n".join(
                [
                    f"Field '{'.'.join(map(str, error['loc']))}' - {error['msg']}"
                    for error in exc.errors()
                ]
            )
        )
        return JSONResponse(status_code=422, content=response_content.model_dump())

    # HTTPException handler
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        response_content = BaseResponseDto(
            code=exc.detail.code if isinstance(exc.detail, BaseResponseDto) else str(exc.status_code),
            message=exc.detail.message if isinstance(exc.detail, BaseResponseDto) else str(exc.detail)
        )
        return JSONResponse(status_code=exc.status_code, content=response_content.model_dump(), headers=exc.headers)
    
    # Starlette HTTPException handler (merged with above if no specific logic differs)
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        response_content = BaseResponseDto(
            code=exc.detail.code if isinstance(exc.detail, BaseResponseDto) else str(exc.status_code),
            message=exc.detail.message if isinstance(exc.detail, BaseResponseDto) else str(exc.detail)
        )
        return JSONResponse(status_code=exc.status_code, content=response_content.model_dump(), headers=exc.headers)

    # Catch-all handler for unexpected errors
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        LOG.error(f"Unexpected error occurred: {exc}")
        return JSONResponse(status_code=500, content=InternalServerError().detail.model_dump())
