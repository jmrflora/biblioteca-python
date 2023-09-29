from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from projetoBiblio.app.emprestimo.models import Emprestimo


class LivroBase(SQLModel):
    Autor: str = Field(min_length=3)
    EP: bool


class Livro(LivroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    exemplares: List["Exemplar"] = Relationship(back_populates="livro")


class LivroCreate(LivroBase):
    pass


class LivroRead(LivroBase):
    id: int


class ExemplarBase(SQLModel):
    livro_id: Optional[int] = Field(default=None, foreign_key="livro.id")


class Exemplar(ExemplarBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    livro: Optional[Livro] = Relationship(back_populates="exemplares")
    usuario_links: List[Emprestimo] = Relationship(back_populates="exemplar")


class ExemplarCreate(ExemplarBase):
    pass


class ExemplarRead(ExemplarBase):
    id: int


class ExemplarReadComLivro(ExemplarRead):
    livro: Optional[LivroRead]


class LivroComExemplares(LivroRead):
    exemplares: List[ExemplarRead] = []
