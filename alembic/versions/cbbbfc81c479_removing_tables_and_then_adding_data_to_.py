"""Removing tables and then adding data to tables

Revision ID: cbbbfc81c479
Revises: your_revision_id
Create Date: 2025-09-19 10:47:29.341555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbbbfc81c479'
down_revision: Union[str, Sequence[str], None] = 'your_revision_id'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema: drop users, doctor_details, and appointments tables."""
    op.drop_table('appointments')
    op.drop_table('doctor_details')
    op.drop_table('users')


def downgrade() -> None:
    """Downgrade schema: recreate users, doctor_details, and appointments tables."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('role', sa.String, nullable=False),
    )

    op.create_table(
        'doctor_details',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('speciality', sa.String, nullable=False),
    )

    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('doctor_id', sa.Integer, nullable=False),
        sa.Column('patient_id', sa.Integer, nullable=False),
        sa.Column('date', sa.String, nullable=False),
    )
