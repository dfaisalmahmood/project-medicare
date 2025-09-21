"""alter users.id from integer to uuid

Revision ID: 0002
Revises: 0001
Create Date: 2025-09-21
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        # Non-Postgres: skip as initial migration will handle String(36); or handle with a separate migration strategy
        return

    # Ensure pgcrypto for gen_random_uuid()
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")

    # 1) Add new UUID column with default
    op.add_column(
        "users",
        sa.Column(
            "id_new",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
    )

    # 2) Backfill existing rows (ensure value present)
    op.execute("UPDATE users SET id_new = gen_random_uuid() WHERE id_new IS NULL;")

    # 3) Drop old PK and column, rename new to id, recreate PK
    op.drop_constraint("users_pkey", "users", type_="primary")
    op.drop_column("users", "id")
    op.alter_column("users", "id_new", new_column_name="id")
    op.create_primary_key("users_pkey", "users", ["id"])

    # 4) Optional: drop server default
    op.alter_column("users", "id", server_default=None)


def downgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name != "postgresql":
        return

    # Reverse: add integer id back (will generate new integers)
    op.add_column("users", sa.Column("id_old", sa.Integer(), nullable=False))
    # Backfill with row_number() over some order for deterministic integers
    op.execute(
        """
        WITH numbered AS (
            SELECT id, ROW_NUMBER() OVER (ORDER BY created_at NULLS FIRST, email) AS rn
            FROM users
        )
        UPDATE users u
        SET id_old = n.rn
        FROM numbered n
        WHERE u.id = n.id;
        """
    )
    op.drop_constraint("users_pkey", "users", type_="primary")
    op.drop_column("users", "id")
    op.alter_column("users", "id_old", new_column_name="id")
    op.create_primary_key("users_pkey", "users", ["id"])
