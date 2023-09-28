from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session

from projetoBiblio.app.core.db import get_session
from projetoBiblio.app.pessoas.models import UsuarioCreate, UsuarioRead, Usuario
from projetoBiblio.app.core.hasher import Hasher

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/')
def get_all():
    return {
        "mensagem": "ok"
    }


@router.post('/usuario', response_model=UsuarioRead)
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
