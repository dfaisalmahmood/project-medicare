import uuid
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Date, String, Enum, ForeignKey, DateTime, func

from app.core.types import GUID
from app.core.db import Base


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, index=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    dob: Mapped[date | None] = mapped_column(Date(), nullable=True)
    gender: Mapped[str | None] = mapped_column(
        Enum("male", "female", "other", name="gender"), nullable=True
    )
    blood_group: Mapped[str | None] = mapped_column(
        Enum("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", name="blood_group"),
        nullable=True,
    )
    ethnicity: Mapped[str | None] = mapped_column(String(100), nullable=True)

    user = relationship("User", back_populates="patients")

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
