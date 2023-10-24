from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Emprestimo, EmprestimoRead, EmprestimoCreate, EmprestimoReadComUsuarioExemplar, Exemplar, Usuario

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]


# todo, fazer um get com emprestimos do usuario atual

@router.get('/', response_model=List[EmprestimoRead])
def get_all_emprestimo(db: db_dependency, admin: user_dependecy, cliente_id: Annotated[int | None, Query()] = None, exemplar_id: Annotated[int | None, Query()] = None):
    
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    statement = select(Emprestimo)
        
    if cliente_id != None:
        db_cliente = db.get(Usuario, cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="usuario nao encontrado")
        statement = statement.where(Emprestimo.usuario == db_cliente)
    
    if exemplar_id != None:
        db_exemplar = db.get(Exemplar, exemplar_id)
        if not db_exemplar:
            raise HTTPException(status_code=404, detail="exemplar not found")
        statement = statement.where(Emprestimo.exemplar == db_exemplar)
        
    db_emprestimos = db.exec(statement).all()
    
    return db_emprestimos

@router.get('/me', response_model=List[EmprestimoRead])
def get_emprestimo_me(db: db_dependency, usuario: user_dependecy):
    db_usuario = db.get(Usuario, usuario.get('id'))
    
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")
    
    db_emprestimos = db.exec(select(Emprestimo).where(Emprestimo.usuario == db_usuario)).all()
    return db_emprestimos

@router.get('/{emprestimo_id}', response_model=EmprestimoReadComUsuarioExemplar)
def get_emprestimo_by_id(db: db_dependency, emprestimo_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    db_emprestimo = db.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="emprestimo not found")
    return db_emprestimo


@router.post('/', response_model=EmprestimoRead)
def create_emprestimo(db: db_dependency, emprestimo_form: EmprestimoCreate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_emprestimo = Emprestimo.from_orm(emprestimo_form)
    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo


@router.delete('/{emprestimo_id}')
def delete_emprestimo(db: db_dependency, emprestimo_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_emprestimo = db.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="emprestimo not found")

    db.delete(db_emprestimo)
    db.commit()
    return {"ok": True}
