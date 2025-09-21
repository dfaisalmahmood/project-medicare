from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.modules.users.service import authenticate_user, create_user, get_user_by_email
from .dto import RegisterRequest, LoginRequest, Token


async def register_user(db: AsyncSession, payload: RegisterRequest):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise ValueError("Email already registered")
    return await create_user(
        db, email=payload.email, password=payload.password, full_name=payload.full_name
    )


async def login_user(db: AsyncSession, username: str, password: str) -> Token:
    user = await authenticate_user(db, username, password)
    if not user:
        raise ValueError("Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return Token(access_token=token)
