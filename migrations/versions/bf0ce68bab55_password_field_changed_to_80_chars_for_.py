"""password field changed to 80 chars for hashing

Revision ID: bf0ce68bab55
Revises: ea30b7ed7dda
Create Date: 2024-12-03 22:48:16.471457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf0ce68bab55'
down_revision = 'ea30b7ed7dda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=15),
               type_=sa.String(length=80),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=80),
               type_=sa.VARCHAR(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###
