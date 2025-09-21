"""create users table

Revision ID: 0001
Revises:
Create Date: 2025-09-20
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use PostgreSQL UUID if available; fallback handled by model layer at runtime
    id_type = postgresql.UUID(as_uuid=True)
    op.create_table(
        "users",
        sa.Column("id", id_type, primary_key=True),
        sa.Column(
            "email", sa.String(length=255), nullable=False, unique=True, index=True
        ),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now()
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("users")
