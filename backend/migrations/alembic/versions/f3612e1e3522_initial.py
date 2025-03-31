"""initial

Revision ID: f3612e1e3522
Revises:
Create Date: 2025-03-31 09:45:43.358893

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f3612e1e3522"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "templates",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("value_data", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("templates")
