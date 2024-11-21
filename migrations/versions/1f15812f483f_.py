"""empty message

Revision ID: 1f15812f483f
Revises: 5bc2801f5b83
Create Date: 2024-11-09 20:24:17.240282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f15812f483f'
down_revision = '5bc2801f5b83'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url_ats', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_column('url_ats')

    # ### end Alembic commands ###