from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import Livro, LivroRead, LivroCreate, LivroUpdate, LivroComExemplares, Exemplar, \
    ExemplarRead, \
    ExemplarCreate, ExemplarReadComLivro

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[LivroRead])
def get_all_livros(db: db_dependency):
    db_livros = db.exec(select(Livro)).all()
    return db_livros


@router.get('/{livro_id}', response_model=LivroComExemplares)
def get_livro_by_id(db: db_dependency, livro_id: int):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro nao encontrado")

    return db_livro


@router.patch('/{livro_id}', response_model=LivroComExemplares)
def update_livro(db: db_dependency, livro_id: int, livro_update_form: LivroUpdate):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro not found")

    livro_data = livro_update_form.dict(exclude_unset=True)
    for key, value in livro_data.items():
        setattr(db_livro, key, value)
    """""
    print(db_livro.nome)
    print(db_livro.Autor)
    print(db_livro.EP)
    """
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro


@router.post('/', response_model=LivroRead)
def create_livro(db: db_dependency, livro_form: LivroCreate):
    db_livro = Livro.from_orm(livro_form)
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro


@router.delete('/{livro_id}')
def delete_livro(db: db_dependency, livro_id: int):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro not found")

    db.delete(db_livro)
    db.commit()
    return {"ok": True}


@router.get('/exemplar/livro/{livro_id}', response_model=List[ExemplarRead])
def get_all_por_livro_id(db: db_dependency, livro_id: int):
    db_exemplares = db.exec(select(Exemplar).where(Exemplar.livro_id == livro_id)).all()
    return db_exemplares


@router.get('/exemplar/{exemplar_id}', response_model=ExemplarReadComLivro)
def get_exemplar_por_id(db: db_dependency, exemplar_id: int):
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not exemplar_id:
        raise HTTPException(status_code=404, detail="exemplar nao encontrado")

    return db_exemplar


@router.post('/exemplar', response_model=ExemplarRead)
def create_exemplar(db: db_dependency, exempar_form: ExemplarCreate):
    db_exemplar = Exemplar.from_orm(exempar_form)
    db.add(db_exemplar)
    db.commit()
    db.refresh(db_exemplar)
    return db_exemplar


@router.delete('/exemplar/{exemplar_id}')
def delete_exemplar(db: db_dependency, exemplar_id: int):
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not db_exemplar:
        raise HTTPException(status_code=404, detail="exemplar not found")

    db.delete(db_exemplar)
    db.commit()
    return {"ok": True}
