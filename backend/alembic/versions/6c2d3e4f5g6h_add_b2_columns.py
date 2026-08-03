"""Add Backblaze B2 URL columns to episodes

Revision ID: 6c2d3e4f5g6h
Revises: 5b1c2d3e4f5g
Create Date: 2026-08-03 09:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "6c2d3e4f5g6h"
down_revision = "5b1c2d3e4f5g"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add B2 URL columns to episodes table."""
    op.add_column("episodes", sa.Column("b2_manifest_url", sa.Text(), nullable=True))
    op.add_column("episodes", sa.Column("b2_video_url", sa.Text(), nullable=True))
    op.add_column("episodes", sa.Column("b2_thumbnail_url", sa.Text(), nullable=True))


def downgrade() -> None:
    """Remove B2 URL columns from episodes table."""
    op.drop_column("episodes", "b2_thumbnail_url")
    op.drop_column("episodes", "b2_video_url")
    op.drop_column("episodes", "b2_manifest_url")