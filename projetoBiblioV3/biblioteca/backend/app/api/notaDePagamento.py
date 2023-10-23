from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import NotaDePagamento, NotaDePagamentoRead, NotaDePagamentoCreate, \
    NotaDePagamentoReadComUsuarioDevolucao, Devolucao, NotaDePagamentoUpdate, Usuario

router = APIRouter()

db_dependendy = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]
# todo, colocar os filtros no /, /me e /{nota_id}

@router.get('/', response_model=List[NotaDePagamentoRead])
def get_all_notas(db: db_dependendy, admin: user_dependecy, cliente_id: Annotated[int | None, Query()] = None):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    statement = select(NotaDePagamento)
    
    if cliente_id != None:
        db_cliente = db.get(Usuario, cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="cliente not found")
        statement = statement.where(NotaDePagamento.usuario == db_cliente)
    
    
    db_notas = db.exec(statement).all()
    return db_notas

@router.get('/me', response_model=List[NotaDePagamentoRead])
def get_all_nota_me(db: db_dependendy, cliente: user_dependecy):
    db_cliente = db.get(Usuario, cliente.get('id'))
    if not db_cliente:
        raise HTTPException(status_code=404, detail="cliente not found")
    if db_cliente.tipo.name != "CLIENTE":
        raise HTTPException(status_code=401, detail="not a cliente")

    db_notas = db.exec(select(NotaDePagamento).where(NotaDePagamento.usuario == db_cliente)).all()
    return db_notas
    
@router.get('/{nota_id}', response_model=NotaDePagamentoReadComUsuarioDevolucao)
def get_nota(db: db_dependendy, nota_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_nota = db.get(NotaDePagamento, nota_id)
    if not db_nota:
        raise HTTPException(status_code=404, detail="nota not found")

    return db_nota


@router.post('/', response_model=NotaDePagamentoRead)
def create_nota(db: db_dependendy, nota_form: NotaDePagamentoCreate, devolucoes_ids: List[int], admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_nota = NotaDePagamento.from_orm(nota_form)
    if not devolucoes_ids:
        raise HTTPException(status_code=404, detail="sem devolucoes")

    for devolucao_id in devolucoes_ids:
        db_devolucao = db.get(Devolucao, devolucao_id)
        if not db_devolucao:
            raise HTTPException(status_code=404, detail="devolucao not found")

        db_nota.devolucoes.append(db_devolucao)

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota


@router.patch('/{nota_id}', response_model=NotaDePagamentoRead)
def update_nota(db: db_dependendy, nota_id: int, nota_update_form: NotaDePagamentoUpdate, devolucoes_ids: List[int], admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_nota = db.get(NotaDePagamento, nota_id)
    if not db_nota:
        raise HTTPException(status_code=404, detail="nota not found")

    for devolucao_id in devolucoes_ids:
        db_devolucao = db.get(Devolucao, devolucao_id)
        if not db_devolucao:
            raise HTTPException(status_code=404, detail="devolucao not found")

        db_nota.devolucoes.append(db_devolucao)

    devolucao_data = nota_update_form.dict(exclude_unset=True)
    for key, value in devolucao_data.items():
        setattr(db_nota, key, value)

    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    return db_nota


@router.delete('/{nota_id}')
def delete_nota(db: db_dependendy, nota_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_nota = db.get(NotaDePagamento, nota_id)
    if not db_nota:
        raise HTTPException(status_code=404, detail="nota not found")
    db.delete(db_nota)
    db.commit()
    return {"ok": True}
