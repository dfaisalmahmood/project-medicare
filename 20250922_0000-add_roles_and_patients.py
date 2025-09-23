"""add roles and patients

Revision ID: add_roles_patients_0001
Revises: fe48c48c62f9
Create Date: 2025-09-22 00:00:00.000000+00:00

"""

import app
from typing import Sequence, Union

from alembic import op, context
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "add_roles_patients_0001"
down_revision: Union[str, Sequence[str], None] = "fe48c48c62f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    schema_upgrades()
    if context.get_x_argument(as_dictionary=True).get("data", None):
        data_upgrades()


def downgrade():
    if context.get_x_argument(as_dictionary=True).get("data", None):
        data_downgrades()
    schema_downgrades()


def schema_upgrades():
    # Add role enum and column to users
    role_enum = sa.Enum("user", "superadmin", name="role")
    role_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "users", sa.Column("role", role_enum, nullable=False, server_default="user")
    )
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)

    # Create gender and blood_group enums
    gender_enum = sa.Enum("male", "female", "other", name="gender")
    gender_enum.create(op.get_bind(), checkfirst=True)
    blood_enum = sa.Enum(
        "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", name="blood_group"
    )
    blood_enum.create(op.get_bind(), checkfirst=True)

    # Create patients table
    op.create_table(
        "patients",
        sa.Column("id", app.core.types.GUID(length=36), nullable=False),
        sa.Column("user_id", app.core.types.GUID(length=36), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("dob", sa.Date(), nullable=True),
        sa.Column("gender", gender_enum, nullable=True),
        sa.Column("blood_group", blood_enum, nullable=True),
        sa.Column("ethnicity", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_patients_id"), "patients", ["id"], unique=False)
    op.create_index(op.f("ix_patients_user_id"), "patients", ["user_id"], unique=False)


def schema_downgrades():
    op.drop_index(op.f("ix_patients_user_id"), table_name="patients")
    op.drop_index(op.f("ix_patients_id"), table_name="patients")
    op.drop_table("patients")

    # Drop users.role
    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_column("users", "role")

    # Drop enums
    bind = op.get_bind()
    sa.Enum(name="gender").drop(bind, checkfirst=True)
    sa.Enum(name="blood_group").drop(bind, checkfirst=True)
    sa.Enum(name="role").drop(bind, checkfirst=True)


def data_upgrades():
    pass


def data_downgrades():
    pass
