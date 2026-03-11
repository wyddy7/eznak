"""add dataset_source_channel_id to channels

Revision ID: 787
Revises: 786
Create Date: 2026-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "787"
down_revision: Union[str, Sequence[str], None] = "786"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "channels",
        sa.Column(
            "dataset_source_channel_id",
            sa.UUID(),
            sa.ForeignKey("channels.id"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("channels", "dataset_source_channel_id")
