from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logger import LOG
from app.schemas.base import BaseResponseDto
from app.errors.error import InternalServerError



def register_error_handlers(app: FastAPI):
    # Validation error handler
    @app.exception_handler(RequestValidationError)
    async def _validation_exception(request: Request, exc: RequestValidationError):
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
    
    # Unified HTTPException handler for both FastAPI and Starlette exceptions
    @app.exception_handler(HTTPException)
    @app.exception_handler(StarletteHTTPException)
    async def _http_exception(request: Request, exc: StarletteHTTPException):
        response_content = BaseResponseDto(
            code=exc.detail.code if isinstance(exc.detail, BaseResponseDto) else str(exc.status_code),
            message=exc.detail.message if isinstance(exc.detail, BaseResponseDto) else str(exc.detail)
        )
        return JSONResponse(status_code=exc.status_code, content=response_content.model_dump(), headers=exc.headers)

    # Catch-all handler for unexpected errors
    @app.exception_handler(Exception)
    async def _global_exception(request: Request, exc: Exception):
        LOG.error(f"Unexpected error occurred: {exc}", exc_info=True)
        return JSONResponse(status_code=500, content=InternalServerError().detail.model_dump())
