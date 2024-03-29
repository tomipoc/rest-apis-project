"""empty message

Revision ID: 96741c69af01
Revises: af458f9beeac
Create Date: 2022-11-25 08:07:48.869219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96741c69af01'
down_revision = 'af458f9beeac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.drop_column('description')

    # ### end Alembic commands ###
