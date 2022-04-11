"""Add foreign key to posts table

Revision ID: a641c714b48b
Revises: 82974c9e55bb
Create Date: 2022-04-11 09:02:07.843071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a641c714b48b'
down_revision = '82974c9e55bb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("fk_posts_users",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("fk_posts_users", table_name="posts")
    op.drop_column("posts", "owner_id")
