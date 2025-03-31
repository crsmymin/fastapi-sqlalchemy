"""add user role

Revision ID: 9a724a1d1a8d
Revises: f5f8d374f9cc
Create Date: 2025-03-31 16:42:00.689035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a724a1d1a8d'
down_revision: Union[str, None] = 'f5f8d374f9cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
