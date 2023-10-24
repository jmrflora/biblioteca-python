from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Livro, LivroRead, LivroCreate, LivroUpdate, LivroComExemplares, Exemplar, \
    ExemplarRead, \
    ExemplarCreate, ExemplarReadComLivro, Usuario, ExemplarReadComLivroEmprestimo, ExemplarReadComLivroReserva

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/', response_model=List[ExemplarRead])
def get_all_exemplares_por_Livro(db: db_dependency, admin: user_dependecy, livro_id: Annotated[int, Query()]):
    db_livro = db.get(Livro, livro_id)
    if not db_livro:
        raise HTTPException(status_code=404, detail="livro not found")
    
    db_exemplares = db.exec(select(Exemplar).where(Exemplar.livro == db_livro)).all()
    return db_exemplares

@router.get('/emprestimos/{exemplar_id}', response_model=ExemplarReadComLivroEmprestimo)
def get_exemplar_por_id_com_emprestimo(db: db_dependency, exemplar_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not exemplar_id:
        raise HTTPException(status_code=404, detail="exemplar nao encontrado")

    return db_exemplar

@router.get('/reservas/{exemplar_id}', response_model=ExemplarReadComLivroReserva)
def get_exemplar_por_id_com_reserva(db: db_dependency, exemplar_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not exemplar_id:
        raise HTTPException(status_code=404, detail="exemplar nao encontrado")

    return db_exemplar


@router.get('/{exemplar_id}', response_model=ExemplarReadComLivro)
def get_exemplar_por_id(db: db_dependency, exemplar_id: int):
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not exemplar_id:
        raise HTTPException(status_code=404, detail="exemplar nao encontrado")

    return db_exemplar


@router.post('/', response_model=ExemplarRead)
def create_exemplar(db: db_dependency, exempar_form: ExemplarCreate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_exemplar = Exemplar.from_orm(exempar_form)
    db.add(db_exemplar)
    db.commit()
    db.refresh(db_exemplar)
    return db_exemplar

@router.delete('/{exemplar_id}')
def delete_exemplar(db: db_dependency, exemplar_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_exemplar = db.get(Exemplar, exemplar_id)
    if not db_exemplar:
        raise HTTPException(status_code=404, detail="exemplar not found")

    db.delete(db_exemplar)
    db.commit()
    return {"ok": True}

