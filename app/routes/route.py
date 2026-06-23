from fastapi import APIRouter

from app.routes.auth import AUTH_ROUTER
from app.routes.v1.v1_route import API_V1_ROUTER


# Router for the entire versioned API
API_ROUTER = APIRouter(prefix="/api")

# Include all routers from the endpoints
API_ROUTER.include_router(AUTH_ROUTER)
API_ROUTER.include_router(API_V1_ROUTER)
