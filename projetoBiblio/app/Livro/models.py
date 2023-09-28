from typing import Optional
from sqlmodel import Field, SQLModel


class LivroBase(SQLModel):
    Autor: str = Field(min_length=3)
    EP: bool


class Livro(LivroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

