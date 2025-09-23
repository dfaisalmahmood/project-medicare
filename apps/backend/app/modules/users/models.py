import uuid
from sqlalchemy import Column, String, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.types import GUID

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    # Use platform-aware GUID type (native UUID on Postgres)
    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, index=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(
        Enum("user", "superadmin", name="role"),
        nullable=False,
        server_default="user",
        index=True,
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    patients = relationship(
        "Patient", back_populates="user", cascade="all, delete-orphan"
    )
