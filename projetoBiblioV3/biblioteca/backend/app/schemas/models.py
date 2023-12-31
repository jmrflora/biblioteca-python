import enum
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, condecimal
from sqlmodel import SQLModel, Field, Relationship, Enum, Column


class HealthCheck(BaseModel):
    nome: str
    version: str

class EmprestimoBase(SQLModel):
    exemplar_id: Optional[int] = Field(default=None, foreign_key="exemplar.id")
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id")


class Emprestimo(EmprestimoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    exemplar: "Exemplar" = Relationship(back_populates="usuario_links")
    usuario: "Usuario" = Relationship(back_populates="exemplar_links")

    # devolucao_id: Optional[int] = Field(default=None, foreign_key="devolucao.id", nullable=True)
    devolucao: Optional["Devolucao"] = Relationship(back_populates="emprestimo")


class EmprestimoCreate(EmprestimoBase):
    pass


class DevolucaoBase(SQLModel):
    emprestimo_id: int = Field(default=None, foreign_key="emprestimo.id")


class Devolucao(DevolucaoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    notaDePagamento_id: Optional[int] = Field(default=None, foreign_key="notadepagamento.id")
    
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    emprestimo: Emprestimo = Relationship(back_populates="devolucao")

    notaDePagamento: Optional["NotaDePagamento"] = Relationship(back_populates="devolucoes")


class DevolucaoCreate(DevolucaoBase):
    pass


class DevolucaoRead(DevolucaoBase):
    id: int
    created_at: datetime
    notaDePagamento_id: Optional[int]


class NotaDePagamentoBase(SQLModel):
    preco: condecimal(max_digits=5, decimal_places=2) = Field(default=10.00)

    usuario_id: int = Field(default=None, foreign_key="usuario.id")


class NotaDePagamento(NotaDePagamentoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    devolucoes: List[Devolucao] = Relationship(back_populates="notaDePagamento")

    usuario: "Usuario" = Relationship(back_populates="notas_de_pagamento")


class NotaDePagamentoRead(NotaDePagamentoBase):
    id: int


class NotaDePagamentoCreate(NotaDePagamentoBase):
    pass


class NotaDePagamentoUpdate(SQLModel):
    preco: Optional[float]


class ReservaBase(EmprestimoBase):
    pass


class Reserva(ReservaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    exemplar: "Exemplar" = Relationship(back_populates="usuario_reserva_links")
    usuario: "Usuario" = Relationship(back_populates="exemplar_reserva_links")


class ReservaCreate(ReservaBase):
    pass


class ReservaRead(ReservaBase):
    id: int


# Livros e exemplares:
class LivroBase(SQLModel):
    nome: str = Field(min_length=3)
    Autor: str = Field(min_length=3)
    EP: bool


class Livro(LivroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    exemplares: List["Exemplar"] = Relationship(back_populates="livro")


class LivroCreate(LivroBase):
    pass


class LivroRead(LivroBase):
    id: int


class LivroUpdate(SQLModel):
    nome: Optional[str] = None
    Autor: Optional[str] = None
    EP: Optional[bool] = False


class ExemplarBase(SQLModel):
    livro_id: Optional[int] = Field(default=None, foreign_key="livro.id")


class Exemplar(ExemplarBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    livro: Optional[Livro] = Relationship(back_populates="exemplares")

    usuario_links: List[Emprestimo] = Relationship(back_populates="exemplar")

    usuario_reserva_links: List[Reserva] = Relationship(back_populates="exemplar")


class ExemplarCreate(ExemplarBase):
    pass


class ExemplarRead(ExemplarBase):
    id: int


class ExemplarReadComLivro(ExemplarRead):
    livro: Optional[LivroRead]



class LivroComExemplares(LivroRead):
    exemplares: List[ExemplarRead] = []


# ____________________________________________________________Pessoas______________________________________________________________________
class Role(enum.Enum):
    ADMIN = 'admin'
    CLIENTE = 'cliente' 




class Pessoa(SQLModel):
    nome: str = Field(min_length=3, nullable=False)
    email: str = Field(min_length=3, nullable=False)


class UsuarioBase(Pessoa):
    endereco: str = Field(min_length=3, nullable=False)
    telefone: str = Field(min_length=3)
    tipo: Role = Field(sa_column=Column(Enum(Role)))
    

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    exemplar_links: List[Emprestimo] = Relationship(back_populates="usuario")

    exemplar_reserva_links: List[Reserva] = Relationship(back_populates="usuario")

    notas_de_pagamento: List[NotaDePagamento] = Relationship(back_populates="usuario")


class UsuarioRead(UsuarioBase):
    id: int


class UsuarioCreate(Pessoa):
    endereco: str = Field(min_length=3, nullable=False)
    telefone: str = Field(min_length=3) 
    senha: str = Field(min_length=3)


class UsuarioUpdate(SQLModel):
    nome: Optional[str]
    email: Optional[str]
    endereco: Optional[str]
    telefone: Optional[str]


# tem que ser aqui se no tem erro com pydantic

class ReservaReadComExemplar(ReservaRead):
    exemplar: Optional[ExemplarRead]

class ReservaReadComUsuarioExemplar(ReservaRead):
    usuario: Optional[UsuarioRead]
    exemplar: Optional[ExemplarRead]


class DevolucaoReadComEmprestimo(DevolucaoRead):
    emprestimo: Emprestimo


class NotaDePagamentoReadComUsuarioDevolucao(NotaDePagamentoRead):
    usuario: Optional[UsuarioRead]
    devolucoes: List[DevolucaoRead]


class EmprestimoRead(EmprestimoBase):
    id: int 
    created_at: datetime


class EmprestimoReadComUsuarioExemplar(EmprestimoRead):
    usuario: Optional[UsuarioRead]
    exemplar: Optional[ExemplarRead]

class EmprestimoMe(EmprestimoRead):
    livro: LivroRead
    


class ExemplarReadComLivroEmprestimo(ExemplarReadComLivro):
    usuario_links: list[EmprestimoRead]
    
class ExemplarReadComLivroReserva(ExemplarReadComLivro):
    usuario_reserva_links: List[ReservaRead]