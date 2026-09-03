"""initial migration

Revision ID: 635bcf7d8ae9
Revises: 
Create Date: 2026-09-02 18:58:06.592909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '635bcf7d8ae9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'songs',
        sa.Column('key', sa.String(length=10), nullable=True)
    )

    op.add_column(
        'songs',
        sa.Column('bpm', sa.Integer(), nullable=True)
    )

    op.alter_column(
        'user',
        'role',
        existing_type=sa.TEXT(),
        type_=sa.String(),
        existing_nullable=True,
        existing_server_default=sa.text("'user'::text")
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.alter_column(
        'user',
        'role',
        existing_type=sa.String(),
        type_=sa.TEXT(),
        existing_nullable=True,
        existing_server_default=sa.text("'user'::text")
    )

    op.drop_column('songs', 'bpm')
    op.drop_column('songs', 'key')