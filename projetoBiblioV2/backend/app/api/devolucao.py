from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import Devolucao, DevolucaoRead, DevolucaoCreate, DevolucaoReadComEmprestimo

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[DevolucaoRead])
def get_all_devolucao(db: db_dependency):
    db_devolucoes = db.exec(select(Devolucao)).all()
    return db_devolucoes


@router.get('/{devolucao_id}', response_model=DevolucaoReadComEmprestimo)
def get_devolucao(db: db_dependency, devolucao_id: int):
    db_devolucao = db.get(Devolucao, devolucao_id)
    if not db_devolucao:
        raise HTTPException(status_code=404, detail="devolucao not found")

    return db_devolucao


@router.post('/', response_model=DevolucaoRead)
def create_devolucao(db: db_dependency, devolucao_form: DevolucaoCreate):
    db_devolucao = Devolucao.from_orm(devolucao_form)
    db.add(db_devolucao)
    db.commit()
    db.refresh(db_devolucao)
    return db_devolucao


@router.delete('/{devolucao_id}')
def delete_devolucao(db: db_dependency, devolucao_id: int):
    db_devolucao = db.get(Devolucao, devolucao_id)
    if not db_devolucao:
        raise HTTPException(status_code=404, detail="devolucao not found")

    db.delete(db_devolucao)
    db.commit()
    return {"ok": True}

