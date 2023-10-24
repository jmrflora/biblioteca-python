from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Devolucao, DevolucaoRead, DevolucaoCreate, DevolucaoReadComEmprestimo, Emprestimo, Exemplar, Usuario

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/', response_model=List[DevolucaoRead])
def get_all_devolucao(db: db_dependency, admin: user_dependecy, cliente_id: Annotated[int | None, Query()] = None, exemplar_id: Annotated[int | None, Query()] = None):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    statement = select(Devolucao)
    
    if cliente_id != None:
        db_cliente = db.get(Usuario, cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="cliente not found")
        
        statement = statement.where(Devolucao.emprestimo.has(usuario=db_cliente))
        # statement = statement.where(Devolucao.emprestimo.usuario == db_cliente)
        
    if exemplar_id != None:
        db_exemplar= db.get(Exemplar, exemplar_id)
        if not db_exemplar:
            raise HTTPException(status_code=404, detail="exemplar not found")
        statement = statement.where(Devolucao.emprestimo.has(exemplar=db_exemplar))
        
        
    db_devolucoes = db.exec(statement).all()
    return db_devolucoes

@router.get('/me', response_model=List[DevolucaoReadComEmprestimo])
def get_devolucao_me(db: db_dependency, usuario: user_dependecy):
    db_cliente = db.get(Usuario, usuario.get('id'))
    if not db_cliente:
        raise HTTPException(status_code=404, detail="cliente not found")
    if db_cliente.tipo.value != "cliente":
        raise HTTPException(status_code=401, detail="not a cliente")
    
    db_devolucoes = db.exec(select(Devolucao).where(Devolucao.emprestimo.has(usuario=db_cliente)))
    return db_devolucoes

@router.get('/emprestimo/{emprestimo_id}', response_model=DevolucaoReadComEmprestimo)
def get_devolucao_por_emprestimoId(db: db_dependency, admin: user_dependecy, emprestimo_id: int):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_emprestimo = db.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="emprestimo not found")
    
    db_devolucao = db.exec(select(Devolucao).where(Devolucao.emprestimo == db_emprestimo)).first()
    if not db_devolucao:
        raise HTTPException(status_code=404, detail="devolucao not found")
    return db_devolucao

@router.get('/{devolucao_id}', response_model=DevolucaoReadComEmprestimo)
def get_devolucao(db: db_dependency, devolucao_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_devolucao = db.get(Devolucao, devolucao_id)
    if not db_devolucao:
        raise HTTPException(status_code=404, detail="devolucao not found")

    return db_devolucao


@router.post('/', response_model=DevolucaoRead)
def create_devolucao(db: db_dependency, devolucao_form: DevolucaoCreate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_devolucao = Devolucao.from_orm(devolucao_form)
    db.add(db_devolucao)
    db.commit()
    db.refresh(db_devolucao)
    return db_devolucao


@router.delete('/{devolucao_id}')
def delete_devolucao(db: db_dependency, devolucao_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_devolucao = db.get(Devolucao, devolucao_id)
    if not db_devolucao:
        raise HTTPException(status_code=404, detail="devolucao not found")

    db.delete(db_devolucao)
    db.commit()
    return {"ok": True}

