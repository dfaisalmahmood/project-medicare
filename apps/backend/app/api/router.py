from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router


api_router = APIRouter()

# Public auth endpoints
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Protected/user-related endpoints
api_router.include_router(users_router, prefix="/users", tags=["users"])
