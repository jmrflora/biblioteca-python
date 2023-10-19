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


@router.get('/cliente/all', response_model=List[UsuarioRead])
def get_all_cliente(db: db_dependency, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    usuarios = db.exec(select(Usuario).where(Usuario.tipo == Role.CLIENTE)).all()
    return usuarios

    
@router.get('/admin/all', response_model=List[UsuarioRead])
def get_all_admin(db: db_dependency, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    usuarios = db.exec(select(Usuario).where(Usuario.tipo == Role.ADMIN)).all()
    return usuarios

@router.get('/me', response_model=UsuarioRead)
def get_usuario(db: db_dependency, usuario: user_dependecy):
    db_usuario = db.get(Usuario, usuario.get('id'))
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario

@router.get('/{usuario_id}', response_model=UsuarioRead)
def get_usuario_id(db: db_dependency, usuario_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return db_usuario



@router.post('/cliente', response_model=UsuarioRead)
def criando_usuario_cliente(usuario_form: UsuarioCreate, db: db_dependency, admin: user_dependecy):
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

@router.post('/admin', response_model=UsuarioRead)
def criando_usuario_admin(usuario_form: UsuarioCreate, db: db_dependency, admin: user_dependecy):
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
        tipo=Role.ADMIN
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.patch('/me', response_model=UsuarioRead)
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


@router.patch('/cliente/{usuario_id}/', response_model=UsuarioRead)
def update_usuario_id_cliente(db: db_dependency, admin: user_dependecy, usuario_update_form: UsuarioUpdate, usuario_id: int):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")
    if db_usuario.tipo != Role.CLIENTE:
        raise HTTPException(status_code=404, detail="endpoint exclusivo para alterar clientes")
    usuario_data = usuario_update_form.dict(exclude_unset=True)
    
    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.patch('/admin/{usuario_id}/', response_model=UsuarioRead)
def update_usuario_id_admin(db: db_dependency, admin: user_dependecy, usuario_update_form: UsuarioUpdate, usuario_id: int):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="admin nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")
    if db_usuario.tipo != Role.ADMIN:
        raise HTTPException(status_code=404, detail="endpoint exclusivo para alterar admins")
    usuario_data = usuario_update_form.dict(exclude_unset=True)
    
    for key, value in usuario_data.items():
        setattr(db_usuario, key, value)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete('/cliente/{usuario_id}')
def delete_usuario_cliente(db: db_dependency, usuario_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")

    if db_usuario.tipo != Role.CLIENTE:
        raise HTTPException(status_code=404, detail="endpoint exclusivo para excluir clientes")
                
    db.delete(db_usuario)
    db.commit()
    return {"ok": True}

@router.delete('/admin/{usuario_id}')
def delete_usuario_admin(db: db_dependency, usuario_id: int, admin: user_dependecy):
    db_admin = db.get(Usuario, admin.get('id'))
    if not db_admin:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if db_admin.tipo.value != "admin":
        raise HTTPException(status_code=401, detail="not an admin")
    
    db_usuario = db.get(Usuario, usuario_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="usuario not found")

    if db_usuario.tipo != Role.ADMIN:
        raise HTTPException(status_code=404, detail="endpoint exclusivo para excluir admins")
                
    db.delete(db_usuario)
    db.commit()
    return {"ok": True}