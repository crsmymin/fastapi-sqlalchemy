"""add user role

Revision ID: 5eec8128b94c
Revises: 9a724a1d1a8d
Create Date: 2025-03-31 16:51:47.334522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5eec8128b94c'
down_revision: Union[str, None] = '9a724a1d1a8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('articles', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('articles', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=False))
    op.alter_column('users', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_column('users', 'role')
    op.alter_column('articles', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('articles', 'user_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###
