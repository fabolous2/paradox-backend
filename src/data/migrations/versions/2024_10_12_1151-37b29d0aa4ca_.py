"""empty message

Revision ID: 37b29d0aa4ca
Revises: ecb7fc98be89
Create Date: 2024-10-12 11:51:31.115044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37b29d0aa4ca'
down_revision: Union[str, None] = 'ecb7fc98be89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('game', sa.Column('web_app_place', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('game', 'web_app_place')
    # ### end Alembic commands ###
