from typing import Optional
from pydantic import EmailStr, validate_email
from sqlmodel import Field, SQLModel


class Pessoa(SQLModel):
    nome: str = Field(min_length=3, nullable=False)
    email: str = Field(min_length=3, nullable=False)


class UsuarioBase(Pessoa):
    endereco: str = Field(min_length=3, nullable=False)
    telefone: str = Field(min_length=3)


class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


class UsuarioRead(UsuarioBase):
    id: int


class UsuarioCreate(UsuarioBase):
    senha: str = Field(min_length=3)

