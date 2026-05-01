"""Adding users table

Revision ID: 23fa98cec693
Revises: 4e7a87253067
Create Date: 2025-09-19 11:06:38.576687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '23fa98cec693'
down_revision: Union[str, Sequence[str], None] = '4e7a87253067'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("DROP TABLE IF EXISTS users CASCADE;")

    # Create users table (minimal version)
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False),
    )



def downgrade() -> None:
    """Downgrade schema."""

    # Drop users table
    op.drop_table('users')
