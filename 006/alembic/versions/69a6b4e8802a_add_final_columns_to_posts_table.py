"""Add final columns to posts table

Revision ID: 69a6b4e8802a
Revises: a641c714b48b
Create Date: 2022-04-11 09:11:23.204847

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69a6b4e8802a'
down_revision = 'a641c714b48b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")
    )
    op.add_column("posts",
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()"))
    )


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
