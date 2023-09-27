from typing import Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session


from projetoBiblio.app.core.db import get_session


router = APIRouter()


db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/')
def get_all():
    return {
        "mensagem": "ok"
    }
