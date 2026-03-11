"""add prompt_templates table and prompt_template_id to channels

Revision ID: 788
Revises: 787
Create Date: 2026-03-11

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "788"
down_revision: Union[str, Sequence[str], None] = "787"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "prompt_templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("generator_system", sa.Text(), nullable=False),
        sa.Column("generator_user_template", sa.Text(), nullable=False),
        sa.Column("critic_system", sa.Text(), nullable=False),
        sa.Column("critic_user_template", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_prompt_templates_name"),
    )
    op.add_column(
        "channels",
        sa.Column(
            "prompt_template_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("prompt_templates.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("channels", "prompt_template_id")
    op.drop_table("prompt_templates")
