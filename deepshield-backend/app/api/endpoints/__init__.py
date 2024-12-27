from fastapi import APIRouter
from . import users, content, ai, notifications

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
