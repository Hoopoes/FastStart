import time
import uuid
from fastapi import FastAPI, Request, Response

from app.utils.config_loader import LOG_CONFIG
from app.utils.log_handler import set_log_context
from app.utils.logger import LOG


def middleware_handler(app: FastAPI):

    @app.middleware("http")
    async def _handler(request: Request, call_next):

        # Start time recording after the method check
        start_time = time.perf_counter()

        # Get HTTP method and route
        http_method = request.method
        route = request.scope.get("path", "Unknown")

        kwargs = {}

        if LOG_CONFIG.context.trace_id:
            kwargs["trace_id"] = uuid.uuid4().hex

        if LOG_CONFIG.context.endpoint:
            kwargs["endpoint"] = route

        set_log_context(**kwargs)

        # Process the request and calculate the time taken
        response: Response
        response = await call_next(request)
        # response = await usage_middleware(response=response)
        process_time = time.perf_counter() - start_time

        # Add the process time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        # Skip logging for less useful or internal methods
        if http_method in ["OPTIONS", "HEAD", "TRACE", "CONNECT"]:
            return response

        # Log the processed request with time taken
        LOG.info(f"{http_method} - {route} - {process_time:.2f} s 🚀")

        return response
