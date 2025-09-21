from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.auth.dependencies import get_current_user
from .dto import UserRead
from .models import User


router = APIRouter()


@router.get("/", response_model=List[UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    # Simple list endpoint for demo; in real usage, add pagination
    results = await db.execute(select(User))
    return results.scalars().all()


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user
