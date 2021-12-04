"""add comtent column in posts

Revision ID: 2b4de67e3078
Revises: d287ae25c90d
Create Date: 2021-12-04 20:52:59.554317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2b4de67e3078'
down_revision = 'd287ae25c90d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
