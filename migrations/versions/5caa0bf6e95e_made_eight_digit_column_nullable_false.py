"""made eight_digit column nullable=False

Revision ID: 5caa0bf6e95e
Revises: 19b96580b977
Create Date: 2021-08-11 17:50:30.796977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5caa0bf6e95e'
down_revision = '19b96580b977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('confirmation', 'eight_digit',
               existing_type=sa.VARCHAR(length=8),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('confirmation', 'eight_digit',
               existing_type=sa.VARCHAR(length=8),
               nullable=True)
    # ### end Alembic commands ###