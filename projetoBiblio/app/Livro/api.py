from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from projetoBiblio.app.core.db import get_session
from .models import *

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/livro', response_model=List[LivroRead])
def get_all_livros(db: db_dependency):
    db_livros = db.exec(select(Livro)).all()
    return db_livros


@router.get('/livro/{livro_id}', response_model=LivroComExemplares)
def get_livro_by_id(db: db_dependency, livro_id: int):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro nao encontrado")

    return db_livro


@router.post('/livro', response_model=LivroRead)
def create_livro(db: db_dependency, livro_form: LivroCreate):
    db_livro = Livro.from_orm(livro_form)
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro

