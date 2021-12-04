"""add columns to posts

Revision ID: 03d9ca3f499f
Revises: 8320528d36ec
Create Date: 2021-12-04 20:56:24.922159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03d9ca3f499f'
down_revision = '8320528d36ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'user_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'user_id')
    pass
