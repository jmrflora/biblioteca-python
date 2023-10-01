from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import Reserva, ReservaRead, ReservaCreate, ReservaReadComUsuarioExemplar

router = APIRouter()

db_dependendy = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[ReservaRead])
def get_all_reserva(db: db_dependendy):
    db_reservas = db.exec(select(Reserva)).all()
    return db_reservas


@router.get('/{reserva_id}', response_model=ReservaReadComUsuarioExemplar)
def get_reserva(db: db_dependendy, reserva_id: int):
    db_reserva = db.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="reserva not found")

    return db_reserva


@router.post('/', response_model=ReservaRead)
def create_reserva(db: db_dependendy, reserva_form: ReservaCreate):
    db_reserva = Reserva.from_orm(reserva_form)
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.delete('/{reserva_id}')
def delete_reserva(db: db_dependendy, reserva_id: int):
    db_reserva = db.get(Reserva, reserva_id)
    if not db_reserva:
        raise HTTPException(status_code=404, detail="reserva not found")

    db.delete(db_reserva)
    db.commit()
    return {"ok": True}