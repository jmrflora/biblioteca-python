from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import Admin, AdminRead, AdminCreate
from backend.app.core.hasher import Hasher

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[AdminRead])
def get_all_admins(db: db_dependency):
    db_admins = db.exec(select(Admin)).all()
    return db_admins


@router.get('/{admin_id}', response_model=AdminRead)
def get_admin_by_id(db: db_dependency, admin_id: int):
    db_admin = db.get(Admin, admin_id)
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin not found")
    return db_admin


@router.post('/', response_model=AdminRead)
def create_admin(db: db_dependency, admin_form: AdminCreate):
    db_admin = Admin(
        nome=admin_form.nome,
        email=admin_form.email,
        hashed_password=Hasher.get_password_hash(admin_form.senha)
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin
