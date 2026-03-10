"""init

Revision ID: 001
Revises:
Create Date: 2025-03-10

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    poststatus = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus", create_type=True)
    poststatus.create(op.get_bind(), checkfirst=True)

    # create_type=False — тип уже создан выше, иначе SQLAlchemy попытается создать его снова
    poststatus_col = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus", create_type=False)

    op.create_table(
        "channels",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("telegram_id", sa.String(64), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "posts",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("channel_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", poststatus_col, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["channel_id"], ["channels.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("posts")
    op.drop_table("channels")
    poststatus = postgresql.ENUM("draft", "scheduled", "posted", "failed", name="poststatus")
    poststatus.drop(op.get_bind(), checkfirst=True)
