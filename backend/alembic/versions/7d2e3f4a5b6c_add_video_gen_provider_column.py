"""Add video_gen_provider column to episodes

Revision ID: 7d2e3f4a5b6c
Revises: 6c2d3e4f5g6h
Create Date: 2026-08-03 16:21:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "7d2e3f4a5b6c"
down_revision = "6c2d3e4f5g6h"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add user-selectable video generation provider column."""
    op.add_column(
        "episodes",
        sa.Column("video_gen_provider", sa.String(32), nullable=True),
    )


def downgrade() -> None:
    """Remove the provider column."""
    op.drop_column("episodes", "video_gen_provider")