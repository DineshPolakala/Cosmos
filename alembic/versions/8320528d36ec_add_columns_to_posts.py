"""add columns to posts

Revision ID: 8320528d36ec
Revises: 2b4de67e3078
Create Date: 2021-12-04 20:54:43.381515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8320528d36ec'
down_revision = '2b4de67e3078'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass