"""Make realname column NOT NULL

Revision ID: 5b38437e81a2
Revises: ceda296b64b9
Create Date: 2024-03-14 12:45:56.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b38437e81a2'
down_revision = 'ceda296b64b9'
branch_labels = None
depends_on = None


def upgrade():
    # Заполняем существующие записи значением по умолчанию
    op.execute("UPDATE \"user\" SET realname = 'Anonymous' WHERE realname IS NULL")
    
    # Делаем колонку NOT NULL
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('realname',
               existing_type=sa.String(length=80),
               nullable=False)


def downgrade():
    # Возвращаем колонке возможность быть NULL
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('realname',
               existing_type=sa.String(length=80),
               nullable=True)
