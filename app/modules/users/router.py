from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.modules.auth.dependencies import get_current_user
from .dto import UserRead
from .models import User


router = APIRouter()


@router.get("/", response_model=List[UserRead])
def list_users(db: Session = Depends(get_db)):
    # Simple list endpoint for demo; in real usage, add pagination
    return db.query(User).all()


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
