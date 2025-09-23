from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.rbac import require_superadmin
from .dto import UserRead, UserCreate, UserUpdate
from .models import User


router = APIRouter()


@router.get(
    "/", response_model=List[UserRead], dependencies=[Depends(require_superadmin)]
)
async def list_users(db: AsyncSession = Depends(get_db)):
    results = await db.execute(select(User))
    return results.scalars().all()


@router.get("/me", response_model=UserRead)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_superadmin)],
)
async def create_user_endpoint(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )
    from .service import create_user as svc_create_user

    user = await svc_create_user(
        db,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
    )
    return user


@router.get(
    "/{user_id}", response_model=UserRead, dependencies=[Depends(require_superadmin)]
)
async def get_user_endpoint(user_id: str, db: AsyncSession = Depends(get_db)):
    from .service import get_user_by_id

    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put(
    "/{user_id}", response_model=UserRead, dependencies=[Depends(require_superadmin)]
)
async def update_user_endpoint(
    user_id: str, payload: UserUpdate, db: AsyncSession = Depends(get_db)
):
    from .service import update_user

    user = await update_user(
        db,
        user_id,
        email=payload.email,
        password=payload.password,
        full_name=payload.full_name,
        role=payload.role,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_superadmin)],
)
async def delete_user_endpoint(user_id: str, db: AsyncSession = Depends(get_db)):
    from .service import delete_user_by_id

    ok = await delete_user_by_id(db, user_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return None
