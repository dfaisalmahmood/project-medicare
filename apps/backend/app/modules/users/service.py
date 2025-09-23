from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from . import models


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    results = await db.execute(select(models.User).filter(models.User.email == email))
    return results.scalars().first()


async def create_user(
    db: AsyncSession,
    email: str,
    password: str,
    full_name: str | None = None,
    role: str | None = None,
) -> models.User:
    user = models.User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name=full_name,
        role=role or "user",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> models.User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def get_user_by_id(db: AsyncSession, user_id) -> models.User | None:
    res = await db.execute(select(models.User).where(models.User.id == user_id))
    return res.scalars().first()


async def list_users(db: AsyncSession) -> list[models.User]:
    res = await db.execute(select(models.User))
    return list(res.scalars().all())


async def update_user(
    db: AsyncSession,
    user_id,
    *,
    email: str | None = None,
    password: str | None = None,
    full_name: str | None = None,
    role: str | None = None,
) -> models.User | None:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    if email is not None:
        user.email = email
    if password is not None:
        user.hashed_password = get_password_hash(password)
    if full_name is not None:
        user.full_name = full_name
    if role is not None:
        user.role = role
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_by_id(db: AsyncSession, user_id) -> bool:
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True
