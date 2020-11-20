"""empty message

Revision ID: ebb6f950eda8
Revises: 0c02edf1edc3
Create Date: 2020-11-19 22:51:34.476969

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ebb6f950eda8'
down_revision = '0c02edf1edc3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('size',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('productcat_id', sa.Integer(), nullable=False),
    sa.Column('productsubcat_id', sa.Integer(), nullable=False),
    sa.Column('desc', sa.String(length=256), nullable=False),
    sa.ForeignKeyConstraint(['productcat_id'], ['productcat.id'], name=op.f('fk_size_productcat_id_productcat')),
    sa.ForeignKeyConstraint(['productsubcat_id'], ['productsubcat.id'], name=op.f('fk_size_productsubcat_id_productsubcat')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_size')),
    sa.UniqueConstraint('id', name=op.f('uq_size_id'))
    )
    op.drop_table('productsize')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productsize',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('productcat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('productsubcat_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('desc', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['productcat_id'], ['productcat.id'], name='productsize_productcat_id_fkey'),
    sa.ForeignKeyConstraint(['productsubcat_id'], ['productsubcat.id'], name='productsize_productsubcat_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='productsize_pkey'),
    sa.UniqueConstraint('id', name='uq_productsize_id')
    )
    op.drop_table('size')
    # ### end Alembic commands ###