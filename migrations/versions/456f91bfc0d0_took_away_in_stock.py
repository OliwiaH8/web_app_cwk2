"""took away in_stock

Revision ID: 456f91bfc0d0
Revises: cb91de8a9079
Create Date: 2024-12-02 20:46:21.401006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '456f91bfc0d0'
down_revision = 'cb91de8a9079'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lego', schema=None) as batch_op:
        batch_op.drop_column('in_stock')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('lego', schema=None) as batch_op:
        batch_op.add_column(sa.Column('in_stock', sa.BOOLEAN(), nullable=True))

    # ### end Alembic commands ###
