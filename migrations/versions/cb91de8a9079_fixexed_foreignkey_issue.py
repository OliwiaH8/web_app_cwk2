"""fixexed foreignkey issue

Revision ID: cb91de8a9079
Revises: 1ada81e330b1
Create Date: 2024-12-02 17:15:27.234129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb91de8a9079'
down_revision = '1ada81e330b1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Wishlist',
    sa.Column('lego_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.ForeignKeyConstraint(['lego_id'], ['lego.id'], ),
    sa.PrimaryKeyConstraint('lego_id', 'customer_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Wishlist')
    # ### end Alembic commands ###
