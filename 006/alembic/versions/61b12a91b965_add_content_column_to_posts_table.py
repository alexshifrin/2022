"""Add content column to posts table

Revision ID: 61b12a91b965
Revises: 9d582cc4ed3c
Create Date: 2022-04-10 16:01:25.373949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61b12a91b965'
down_revision = '9d582cc4ed3c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade():
    op.drop_column("posts", "content")
