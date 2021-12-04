"""create post

Revision ID: 86372226b551
Revises: 
Create Date: 2021-12-04 20:27:15.367211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = '86372226b551'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('post',sa.Column('id', sa.Integer(),nullable=False, primary_key=True),sa.Column('title',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('post')
    pass
