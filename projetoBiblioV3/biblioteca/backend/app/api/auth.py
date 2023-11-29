from datetime import timedelta
import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from backend.app.core.db import get_session
from backend.app.schemas.models import Usuario
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt 
from backend.app.core.hasher import Hasher

router = APIRouter()

SECRET_KEY = '47522f38042f2e33049d3ddf68f4ee2db9f986475aaa49499d2ba800fd78d6e6'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
    
    
db_dependency = Annotated[Session, Depends(get_session)]

class Token(SQLModel):
    access_token: str
    token_type: str
    refresh_token: str

def autenticar_usuario(nome: str, senha: str, db: Session):
    db_usuario  = db.exec(select(Usuario).where(Usuario.nome == nome)).first()
    if not db_usuario:
        return False
    if not Hasher.verify_password(senha, db_usuario.hashed_password):
        return False
    
    return db_usuario


def criar_token(nome: str, usuario_id: int, expires_delta: timedelta):
    encode = {'sub': nome, 'id': usuario_id}
    expires = datetime.datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def criar_refresh_token(nome: str, usuario_id: int, expires_delta: timedelta):
    encode = {'sub': nome, 'id': usuario_id}
    expires = datetime.datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        nome: str = payload.get('sub')
        usuario_id: int = payload.get('id')
        if nome is None or usuario_id is None:
            raise HTTPException(status_code=401, detail="não pude validar usuario")
        return {'nome': nome, 'id': usuario_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="não pude validar usuario")

@router.post("/token", response_model=Token)
def login_para_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    db_usuario = autenticar_usuario(form_data.username, form_data.password, db)
    if not db_usuario:
        raise HTTPException(status_code=401, detail="não pude validar usuario")
    
    token = criar_token(db_usuario.nome, db_usuario.id, timedelta(minutes=20))
    refresh_token = criar_refresh_token(db_usuario.nome, db_usuario.id, timedelta(minutes=60))
    return {'access_token': token, 'token_type': 'bearer', 'refresh_token': refresh_token}

# não estour recriando o refresh token
@router.post("/refresh", response_model=Token)
def refresh_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        nome: str = payload.get('sub')
        usuario_id: int = payload.get('id')
        if nome is None or usuario_id is None:
            raise HTTPException(status_code=401, detail="não pude validar usuario")
        access_token = criar_token(nome, usuario_id, timedelta(minutes=20))
        return {'access_token': access_token, 'token_type': 'bearer', 'refresh_token': refresh_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="não pude validar usuario")

@router.get('/teste')
def teste(usuario: Annotated[dict, Depends(get_current_user)]):
    
    return {'nome': usuario.get('nome')}
