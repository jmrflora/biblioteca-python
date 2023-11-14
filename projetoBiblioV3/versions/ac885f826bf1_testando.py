"""testando

Revision ID: ac885f826bf1
Revises: fb771d9ff690
Create Date: 2023-10-11 21:58:17.136572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ac885f826bf1'
down_revision: Union[str, None] = 'fb771d9ff690'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('devolucao', 'emprestimo_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('emprestimo_devolucao_id_fkey', 'emprestimo', type_='foreignkey')
    op.drop_column('emprestimo', 'devolucao_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('emprestimo', sa.Column('devolucao_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('emprestimo_devolucao_id_fkey', 'emprestimo', 'devolucao', ['devolucao_id'], ['id'])
    op.alter_column('devolucao', 'emprestimo_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###