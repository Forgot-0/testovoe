"""empty message

Revision ID: 6b43ff0d1d28
Revises: 27780b68dc43
Create Date: 2025-04-04 19:40:52.552959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6b43ff0d1d28'
down_revision: Union[str, None] = '27780b68dc43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('logs',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('event_type', sa.String(length=20), nullable=False),
    sa.Column('ip_address', postgresql.INET(), nullable=False),
    sa.Column('secret_key_hash', sa.String(), nullable=False),
    sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'secrets', ['key_hash'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'secrets', type_='unique')
    op.drop_table('logs')
    # ### end Alembic commands ###
