from fastapi import APIRouter

from app.routes.v1.api.user import user_router

# Router for the entire versioned API
API_V1_ROUTER = APIRouter(prefix="/v1")

# Include all routers from the endpoints
API_V1_ROUTER.include_router(user_router, prefix="/user", tags=["User"])

