from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Reserva, ReservaRead, ReservaCreate, ReservaReadComExemplar, ReservaReadComUsuarioExemplar, Role, Usuario

router = APIRouter()

db_dependendy = Annotated[Session, Depends(get_session)]
user_dependecy = Annotated[dict, Depends(get_current_user)]

@router.get('/', response_model=List[ReservaRead])
def get_all_reserva(db: db_dependendy , admin: user_dependecy, cliente_id: Annotated[int | None, Query()] = None):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    if cliente_id == None:
        db_reservas = db.exec(select(Reserva)).all()
    else:
        db_cliente = db.get(Usuario, cliente_id)
        if not db_cliente:
            raise HTTPException(status_code=404, detail="cliente não encontrado")
        db_reservas = db.exec(select(Reserva).where(Reserva.usuario == db_cliente)).all()    
        
    return db_reservas

@router.get('/me', response_model=List[ReservaReadComExemplar])
def get_reserva_me(db: db_dependendy, usuario: user_dependecy):
    db_cliente = db.get(Usuario, usuario.get('id'))
    
    if not db_cliente:
        raise HTTPException(status_code=404, detail="usuario não encontrado")
    if db_cliente.tipo != Role.CLIENTE:
        raise HTTPException(status_code=401, detail="not an client")
    
    db_reservas = db.exec(select(Reserva).where(Reserva.usuario == db_cliente)).all()
    
    return db_reservas

@router.get('/{reserva_id}', response_model=ReservaReadComUsuarioExemplar)
def get_reserva(db: db_dependendy, reserva_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")

    db_reserva = db.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="reserva not found")

    return db_reserva


@router.post('/', response_model=ReservaRead)
def create_reserva(db: db_dependendy, reserva_form: ReservaCreate, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin") 
    
     
    db_reserva = Reserva.from_orm(reserva_form)
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.delete('/{reserva_id}')
def delete_reserva(db: db_dependendy, reserva_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")

    db_reserva = db.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="reserva not found")

    db.delete(db_reserva)
    db.commit()
    return {"ok": True}