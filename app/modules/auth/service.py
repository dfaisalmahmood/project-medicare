from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.modules.users.service import authenticate_user, create_user, get_user_by_email
from .dto import RegisterRequest, LoginRequest, Token


def register_user(db: Session, payload: RegisterRequest):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise ValueError("Email already registered")
    return create_user(
        db, email=payload.email, password=payload.password, full_name=payload.full_name
    )


def login_user(db: Session, payload: LoginRequest) -> Token:
    user = authenticate_user(db, payload.email, payload.password)
    if not user:
        raise ValueError("Incorrect email or password")
    token = create_access_token({"sub": user.email})
    return Token(access_token=token)
