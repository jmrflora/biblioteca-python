from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, SQLModel, Field
from backend.app.api.auth import get_current_user

from backend.app.core.db import get_session
from backend.app.schemas.models import Role, UsuarioCreate, UsuarioRead, Usuario, UsuarioUpdate
from backend.app.core.hasher import Hasher

router = APIRouter()


user_dependecy = Annotated[dict, Depends(get_current_user)]
db_dependency = Annotated[Session, Depends(get_session)]


class Senha(SQLModel):
    senha_texto: str = Field(min_length=3)

"""""
@router.get('/cliente/all/', response_model=List[UsuarioRead])
def get_all(db: db_dependency, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    usuarios = db.exec(select(Usuario)).all()
    return usuarios


@router.get('/cliente/{usuario_id}/', response_model=UsuarioRead)
def get_usuario(db: db_dependency, usuario_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario

@router.post('/cliente/', response_model=UsuarioRead)
def criando_usuario(usuario_form: UsuarioCreate, db: db_dependency, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
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


@router.delete('/cliente/{usuario_id}/')
def delete_usuario(db: db_dependency, usuario_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")

    db.delete(db_usuario)
    db.commit()
    return {"ok": True}
"""