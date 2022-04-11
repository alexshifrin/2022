"""Add user table

Revision ID: 82974c9e55bb
Revises: 61b12a91b965
Create Date: 2022-04-11 08:47:11.787087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82974c9e55bb'
down_revision = '61b12a91b965'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )


def downgrade():
    op.drop_table("users")
