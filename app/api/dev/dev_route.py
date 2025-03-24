from fastapi import APIRouter

from app.api.dev.endpoints.log_viewer import log_router

# Router for the entire versioned API
API_DEV_ROUTER = APIRouter(prefix="/dev", tags=["Developer"])

# Include all routers from the endpoints
API_DEV_ROUTER.include_router(log_router, prefix="/server")

