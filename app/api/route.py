from fastapi import APIRouter

from app.api.v1.v1_route import API_V1_ROUTER
from app.api.dev.dev_route import API_DEV_ROUTER


# Router for the entire versioned API
API_ROUTER = APIRouter(prefix="/api")

# Include all routers from the endpoints
API_ROUTER.include_router(API_DEV_ROUTER)
API_ROUTER.include_router(API_V1_ROUTER)
