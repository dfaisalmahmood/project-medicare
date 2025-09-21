import uuid
from sqlalchemy.types import TypeDecorator, CHAR


class GUID(TypeDecorator):
    """Platform-independent GUID/UUID type.

    Uses PostgreSQL's UUID type, otherwise stores as CHAR(36).
    Returns Python uuid.UUID instances in code.
    """

    impl = CHAR(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import UUID as PG_UUID

            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value if dialect.name == "postgresql" else str(value)
        # Accept strings and convert
        try:
            u = uuid.UUID(str(value))
        except Exception:
            raise ValueError("Invalid UUID value for GUID type")
        return u if dialect.name == "postgresql" else str(u)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(str(value))
