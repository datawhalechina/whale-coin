"""Recreate lost migrations

Revision ID: eee8a56ced60
Revises: 39f5ba1accaf
Create Date: 2024-09-25 09:53:41.046602

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eee8a56ced60'
down_revision: Union[str, None] = '39f5ba1accaf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
