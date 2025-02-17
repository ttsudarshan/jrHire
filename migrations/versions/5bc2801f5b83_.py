"""empty message

Revision ID: 5bc2801f5b83
Revises: d66bbb5c8403
Create Date: 2024-10-31 10:08:05.543662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bc2801f5b83'
down_revision = 'd66bbb5c8403'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('job_type', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('introduction', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('compensation_per_hour', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('requirements', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('profile_colors', sa.String(length=100), nullable=True))
        batch_op.alter_column('location',
               existing_type=sa.TEXT(),
               type_=sa.String(length=100),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.alter_column('location',
               existing_type=sa.String(length=100),
               type_=sa.TEXT(),
               existing_nullable=True)
        batch_op.drop_column('profile_colors')
        batch_op.drop_column('requirements')
        batch_op.drop_column('compensation_per_hour')
        batch_op.drop_column('introduction')
        batch_op.drop_column('created_at')
        batch_op.drop_column('job_type')

    # ### end Alembic commands ###
