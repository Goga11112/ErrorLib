"""Make error_id nullable

Revision ID: 72d7ecde3928
Revises: 21632c2dd1ec
Create Date: 2025-02-20 14:48:45.778913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d7ecde3928'
down_revision = '21632c2dd1ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_log', schema=None) as batch_op:
        batch_op.alter_column('error_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin_log', schema=None) as batch_op:
        batch_op.alter_column('error_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
