from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserRead(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str | None = None

    class Config:
        from_attributes = True
