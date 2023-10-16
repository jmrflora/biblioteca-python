"""adicionando devolucao id no emprestimo

Revision ID: fb771d9ff690
Revises: c82c6f5d536a
Create Date: 2023-10-02 10:34:49.660566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'fb771d9ff690'
down_revision: Union[str, None] = 'c82c6f5d536a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.add_column('emprestimo', sa.Column('devolucao_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'emprestimo', 'devolucao', ['devolucao_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'emprestimo', type_='foreignkey')
    op.drop_column('emprestimo', 'devolucao_id')

    # ### end Alembic commands ###