"""Create autogenerate Alembic revision for votes table

Revision ID: 030514f5a44e
Revises: 69a6b4e8802a
Create Date: 2022-04-11 09:34:24.517806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030514f5a44e'
down_revision = '69a6b4e8802a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
