"""create column for post content

Revision ID: e477f4063499
Revises: 86372226b551
Create Date: 2021-12-04 20:34:21.802048

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import null


# revision identifiers, used by Alembic.
revision = 'e477f4063499'
down_revision = '86372226b551'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post',sa.Column('content',sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('post','content')
    pass
