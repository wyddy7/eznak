"""add unique constraint datasets channel_id text

Revision ID: 785
Revises: 784ce0a789f1
Create Date: 2026-03-11

"""
from typing import Sequence, Union

from alembic import op

revision: str = "785"
down_revision: Union[str, Sequence[str], None] = "784ce0a789f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_datasets_channel_id_text",
        "datasets",
        ["channel_id", "text"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_datasets_channel_id_text",
        "datasets",
        type_="unique",
    )
