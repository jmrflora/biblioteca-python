from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

from ..emprestimo.models import Emprestimo


class Pessoa(SQLModel):
    nome: str = Field(min_length=3, nullable=False)
    email: str = Field(min_length=3, nullable=False)


class UsuarioBase(Pessoa):
    endereco: str = Field(min_length=3, nullable=False)
    telefone: str = Field(min_length=3)


class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    exemplar_links: List[Emprestimo] = Relationship(back_populates="usuario")


class UsuarioRead(UsuarioBase):
    id: int


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=3)


class AdminBase(Pessoa):
    pass


class Admin(AdminBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class AdminRead(AdminBase):
    id: int


class AdminCreate(AdminBase):
    senha: str = Field(min_length=3)
