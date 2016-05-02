"""empty message

Revision ID: 6ec7aff6b3f7
Revises: None
Create Date: 2016-03-04 23:04:18.995000

"""

# revision identifiers, used by Alembic.
revision = '6ec7aff6b3f7'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('warning',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('county', sa.String(length=100), nullable=True),
    sa.Column('warning_type', sa.String(length=100), nullable=True),
    sa.Column('station', sa.String(length=100), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('warning_exists', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('warning')
    ### end Alembic commands ###