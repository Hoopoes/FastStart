from config import CONFIG
from fastapi import APIRouter
from app.api.user import user_router


MAIN_ROUTER = APIRouter(prefix=CONFIG.route_prefix)

MAIN_ROUTER.include_router(user_router)