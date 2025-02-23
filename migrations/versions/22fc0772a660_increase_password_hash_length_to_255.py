"""Increase password_hash length to 255

Revision ID: 22fc0772a660
Revises: a613d1c3572c
Create Date: 2025-02-17 13:44:53.987868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22fc0772a660'
down_revision = 'a613d1c3572c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=120),
               existing_nullable=False)

    # ### end Alembic commands ###
