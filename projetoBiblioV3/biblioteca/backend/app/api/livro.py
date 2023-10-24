from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Livro, LivroRead, LivroCreate, LivroUpdate, LivroComExemplares, Exemplar, \
    ExemplarRead, \
    ExemplarCreate, ExemplarReadComLivro, Usuario

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/', response_model=List[LivroRead])
def get_all_livros(db: db_dependency, autor: Annotated[str | None, Query()] = None):
    
    statement = select(Livro)
    
    if autor != None:
        statement = statement.where(Livro.Autor == autor)
    
    db_livros = db.exec(statement).all()
    return db_livros


@router.get('/{livro_id}', response_model=LivroComExemplares)
def get_livro_by_id(db: db_dependency, livro_id: int):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro nao encontrado")

    return db_livro


@router.patch('/{livro_id}', response_model=LivroComExemplares)
def update_livro(db: db_dependency, livro_id: int, livro_update_form: LivroUpdate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
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
def create_livro(db: db_dependency, livro_form: LivroCreate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_livro = Livro.from_orm(livro_form)
    db.add(db_livro)
    db.commit()
    db.refresh(db_livro)
    return db_livro


@router.delete('/{livro_id}')
def delete_livro(db: db_dependency, livro_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro not found")

    db.delete(db_livro)
    db.commit()
    return {"ok": True}




