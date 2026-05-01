"""Initial message

Revision ID: 47b97b013c11
Revises: 
Create Date: 2025-09-17 17:47:41.630724

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '47b97b013c11'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic
revision = 'your_revision_id'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Bind a session to the current connection
    bind = op.get_bind()
    session = Session(bind=bind)

    # Insert users
    session.execute(
        sa.text("""
        INSERT INTO users (username, password, role) VALUES
        ('admin', 'admin123', 'admin'),
        ('doctor1', 'doc123', 'doctor'),
        ('doctor2', 'doc456', 'doctor'),
        ('patient1', 'pat123', 'patient'),
        ('patient2', 'pat456', 'patient');
        """)
    )

    # Insert doctor_details
    session.execute(
        sa.text("""
        INSERT INTO doctor_details (user_id, speciality) VALUES
        ((SELECT id FROM users WHERE username='doctor1'), 'Cardiologist'),
        ((SELECT id FROM users WHERE username='doctor2'), 'Dermatologist');
        """)
    )

    # Insert appointments
    session.execute(
        sa.text("""
        INSERT INTO appointments (doctor_id, patient_id, date) VALUES
        ((SELECT id FROM users WHERE username='doctor1'),
         (SELECT id FROM users WHERE username='patient1'),
         '2025-09-18 10:00:00'),
        ((SELECT id FROM users WHERE username='doctor2'),
         (SELECT id FROM users WHERE username='patient2'),
         '2025-09-18 11:00:00');
        """)
    )

    session.commit()

def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("DELETE FROM appointments"))
    session.execute(sa.text("DELETE FROM doctor_details"))
    session.execute(sa.text("DELETE FROM users"))

    session.commit()
