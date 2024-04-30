"""update tables

Revision ID: a6194cfcfe77
Revises: f8acc412c2b3
Create Date: 2024-04-30 10:00:58.225682

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6194cfcfe77'
down_revision = 'f8acc412c2b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_types',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_type_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'location_types', ['location_type_id'], ['id'])
        batch_op.drop_column('location_type')

    with op.batch_alter_table('tool_locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model', sa.String(length=10), nullable=False))
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tool_locations', schema=None) as batch_op:
        batch_op.drop_column('name')
        batch_op.drop_column('model')

    with op.batch_alter_table('locations', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location_type', sa.VARCHAR(length=10), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('location_type_id')

    op.drop_table('location_types')
    # ### end Alembic commands ###
