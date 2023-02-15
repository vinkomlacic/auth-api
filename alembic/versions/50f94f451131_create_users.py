"""create users and items

Revision ID: 50f94f451131
Revises: 
Create Date: 2023-02-15 22:29:30.943056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50f94f451131'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
