from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.core.db import get_session
from backend.app.schemas.models import UsuarioCreate, UsuarioRead, Usuario
from backend.app.core.hasher import Hasher

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/', response_model=List[UsuarioRead])
def get_all(db: db_dependency):
    usuarios = db.exec(select(Usuario)).all()
    return usuarios


@router.get('/{usuario_id}', response_model=UsuarioRead)
def get_usuario(db: db_dependency, usuario_id: int):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario


@router.post('/', response_model=UsuarioRead)
def criando_usuario(usuario_form: UsuarioCreate, db: db_dependency):
    db_usuario = Usuario(
        nome=usuario_form.email,
        email=usuario_form.email,
        endereco=usuario_form.endereco,
        telefone=usuario_form.telefone,
        hashed_password=Hasher.get_password_hash(usuario_form.senha)
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario