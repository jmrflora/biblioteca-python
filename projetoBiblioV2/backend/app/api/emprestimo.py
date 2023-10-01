from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import Emprestimo, EmprestimoRead, EmprestimoCreate, EmprestimoReadComUsuarioExemplar

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[EmprestimoRead])
def get_all_emprestimo(db: db_dependency):
    db_emprestimos = db.exec(select(Emprestimo)).all()
    return db_emprestimos


@router.get('/{emprestimo_id}', response_model=EmprestimoReadComUsuarioExemplar)
def get_emprestimo_by_id(db: db_dependency, emprestimo_id: int):
    db_emprestimo = db.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="emprestimo not found")
    return db_emprestimo


@router.post('/', response_model=EmprestimoRead)
def create_emprestimo(db: db_dependency, emprestimo_form: EmprestimoCreate):
    db_emprestimo = Emprestimo.from_orm(emprestimo_form)
    db.add(db_emprestimo)
    db.commit()
    db.refresh(db_emprestimo)
    return db_emprestimo


@router.delete('/{emprestimo_id}')
def delete_emprestimo(db: db_dependency, emprestimo_id: int):
    db_emprestimo = db.get(Emprestimo, emprestimo_id)
    if not db_emprestimo:
        raise HTTPException(status_code=404, detail="emprestimo not found")

    db.delete(db_emprestimo)
    db.commit()
    return {"ok": True}
