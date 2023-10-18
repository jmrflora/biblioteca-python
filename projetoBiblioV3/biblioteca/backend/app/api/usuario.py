from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel, Field

from backend.app.core.db import get_session
from backend.app.schemas.models import UsuarioCreate, UsuarioRead, Usuario, UsuarioUpdate, Role
from backend.app.core.hasher import Hasher
from backend.app.api.auth import get_current_user

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]

user_dependecy = Annotated[dict, Depends(get_current_user)]

class Senha(SQLModel):
    senha_texto: str = Field(min_length=3)

# todo make only accessible to admin
@router.get('/all/', response_model=List[UsuarioRead])
def get_all(db: db_dependency):
    usuarios = db.exec(select(Usuario)).all()
    return usuarios

# todo, make only accessible to admin
@router.get('/{usuario_id}/', response_model=UsuarioRead)
def get_usuario(db: db_dependency, usuario_id: int):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario

@router.get('/me/', response_model=UsuarioRead)
def get_usuario(db: db_dependency, usuario: user_dependecy):
    db_usuario = db.get(Usuario, usuario.get('id'))
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario

# todo acessível somente para admin
@router.post('/', response_model=UsuarioRead)
def criando_usuario(usuario_form: UsuarioCreate, db: db_dependency):
    db_usuario = Usuario(
        nome=usuario_form.nome,
        email=usuario_form.email,
        endereco=usuario_form.endereco,
        telefone=usuario_form.telefone,
        hashed_password=Hasher.get_password_hash(usuario_form.senha),
        tipo=Role.CLIENTE
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.patch('/me/', response_model=UsuarioRead)
def update_usuario(db: db_dependency, usuario: user_dependecy, senha: Senha, usuario_update_form: UsuarioUpdate):
    
    db_usuario = db.get(Usuario, usuario.get('id'))
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")

    if not Hasher.verify_password(senha.senha_texto, db_usuario.hashed_password):
        raise HTTPException(status_code=401, detail="senha incorreta")

    usuario_data = usuario_update_form.dict(exclude_unset=True)

    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# todo fazer acessivel somente para admin
@router.delete('/{usuario_id')
def delete_usuario(db: db_dependency, usuario_id: int, senha: Senha):
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")

    if not Hasher.verify_password(senha.senha_texto, db_usuario.hashed_password):
        raise HTTPException(status_code=401, detail="senha incorreta")

    db.delete(db_usuario)
    db.commit()
    return {"ok": True}
