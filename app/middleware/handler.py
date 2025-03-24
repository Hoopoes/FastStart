import time
from app.core.logger import LOG
from fastapi import FastAPI, Request, Response
from app.middleware.usage import usage_middleware



def register_middlewares(app: FastAPI):
    
    @app.middleware("http")
    async def _handler(request: Request, call_next):

        # Get HTTP method and route
        http_method = request.method
        route = request.scope.get("path", "Unknown")

        # Skip logging for less useful or internal methods
        if http_method in ["OPTIONS", "HEAD", "TRACE", "CONNECT"]:
            return await call_next(request)

        # Start time recording after the method check
        start_time = time.perf_counter()

        # Process the request and calculate the time taken
        response: Response
        response = await call_next(request)
        response = await usage_middleware(response=response)
        process_time = time.perf_counter() - start_time

        # Add the process time to response headers
        response.headers["X-Process-Time"] = str(process_time)

        # Log the processed request with time taken
        LOG.info(f"{http_method} - {route} - {process_time:.2f} s 🚀")

        return response