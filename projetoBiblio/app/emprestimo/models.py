from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from ..Livro.models import Exemplar
from ..pessoas.models import Usuario


class EmprestimoBase(SQLModel):
    exemplar_id: Optional[int] = Field(default=None, foreign_key="exemplar.id")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class Emprestimo(EmprestimoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    exemplar: Exemplar = Relationship(back_populates="usuario_links")
    usuario: Usuario = Relationship(back_populates="exemplar_links")





