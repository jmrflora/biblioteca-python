from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class HealthCheck(BaseModel):
    nome: str
    version: str


# Livros e exemplares:
class LivroBase(SQLModel):
    Autor: str = Field(min_length=3)
    EP: bool


class Livro(LivroBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)

    exemplares: List["Exemplar"] = Relationship(back_populates="livro")


class LivroCreate(LivroBase):
    pass


class LivroRead(LivroBase):
    id: int


class ExemplarBase(SQLModel):
    livro_id: Optional[int] = Field(default=None, foreign_key="livro.id")


class Exemplar(ExemplarBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)

    livro: Optional[Livro] = Relationship(back_populates="exemplares")
    # usuario_links: List[Emprestimo] = Relationship(back_populates="exemplar")


class ExemplarCreate(ExemplarBase):
    pass


class ExemplarRead(ExemplarBase):
    id: int


class ExemplarReadComLivro(ExemplarRead):
    livro: Optional[LivroRead]


class LivroComExemplares(LivroRead):
    exemplares: List[ExemplarRead] = []


# Pessoas:
class Pessoa(SQLModel):
    nome: str = Field(min_length=3, nullable=False)
    email: str = Field(min_length=3, nullable=False)


class UsuarioBase(Pessoa):
    endereco: str = Field(min_length=3, nullable=False)
    telefone: str = Field(min_length=3)


class Usuario(UsuarioBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    # exemplar_links: List[Emprestimo] = Relationship(back_populates="usuario")


class UsuarioRead(UsuarioBase):
    id: int


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=3)


class AdminBase(Pessoa):
    pass


class Admin(AdminBase, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class AdminRead(AdminBase):
    id: int


class AdminCreate(AdminBase):
    senha: str = Field(min_length=3)
