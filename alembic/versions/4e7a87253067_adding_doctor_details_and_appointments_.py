"""Adding doctor_details and appointments tables

Revision ID: 4e7a87253067
Revises: cbbbfc81c479
Create Date: 2025-09-19 10:54:56.332669

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e7a87253067'
down_revision: Union[str, Sequence[str], None] = 'cbbbfc81c479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from alembic import op
import sqlalchemy as sa

from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    """Upgrade schema: drop all old tables and recreate only doctor_details + appointments."""

    # Drop all old tables if they exist
    op.execute("DROP TABLE IF EXISTS users CASCADE;")
    op.execute("DROP TABLE IF EXISTS doctors CASCADE;")
    op.execute("DROP TABLE IF EXISTS orders CASCADE;")
    op.execute("DROP TABLE IF EXISTS doctor_details CASCADE;")
    op.execute("DROP TABLE IF EXISTS appointments CASCADE;")

    # Create doctor_details table
    op.create_table(
        'doctor_details',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('doctor_name', sa.String, nullable=False),
        sa.Column('speciality', sa.String, nullable=False),
    )

    # Create appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('patient_name', sa.String, nullable=False),
        sa.Column('date', sa.String, nullable=False),
    )

    # Insert initial rows into doctor_details
    op.execute(
        sa.text(
            "INSERT INTO doctor_details (doctor_name, speciality) VALUES "
            "('Dr. Smith', 'Cardiology'),"
            "('Dr. Johnson', 'Neurology')"
        )
    )

    # Insert initial rows into appointments
    op.execute(
        sa.text(
            "INSERT INTO appointments (patient_name, date) VALUES "
            "('Ali', '2025-09-20'),"
            "('Ahmad', '2025-09-21')"
        )
    )


def downgrade() -> None:
    """Downgrade schema: remove doctor_details + appointments, recreate old doctors + orders."""

    # Drop new tables
    op.drop_table('appointments')
    op.drop_table('doctor_details')

    # Recreate old tables
    op.create_table(
        'orders',
        sa.Column('Age', sa.BigInteger, nullable=True),
    )

    op.create_table(
        'doctors',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('specialization', sa.String, nullable=False),
    )
