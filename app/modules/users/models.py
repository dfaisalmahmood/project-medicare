import uuid
from sqlalchemy import Column, String, DateTime, func
from app.core.types import GUID

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    # Use platform-aware GUID type (native UUID on Postgres)
    id = Column(GUID(), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
