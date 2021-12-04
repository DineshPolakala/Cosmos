"""add posts table

Revision ID: d287ae25c90d
Revises: e7559c549a8b
Create Date: 2021-12-04 20:49:08.714854

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd287ae25c90d'
down_revision = 'e7559c549a8b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass