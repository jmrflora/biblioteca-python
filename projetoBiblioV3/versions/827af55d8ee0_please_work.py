"""please work

Revision ID: 827af55d8ee0
Revises: d83e13ab8149
Create Date: 2023-09-29 17:48:37.626826

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '827af55d8ee0'
down_revision: Union[str, None] = 'd83e13ab8149'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('livro', sa.Column('nome', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('livro', 'nome')
    # ### end Alembic commands ###
