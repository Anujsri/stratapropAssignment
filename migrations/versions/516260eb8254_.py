"""empty message

Revision ID: 516260eb8254
Revises: b609960e7d65
Create Date: 2019-12-16 01:29:24.511287

"""

# revision identifiers, used by Alembic.
revision = '516260eb8254'
down_revision = 'b609960e7d65'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device_info', sa.Column('is_free', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device_info', 'is_free')
    ### end Alembic commands ###
