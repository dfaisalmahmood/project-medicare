from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    role: str | None = None


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None = None
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    role: str | None = None
