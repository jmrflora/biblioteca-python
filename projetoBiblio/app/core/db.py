from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel

from projetoBiblio.app import settings
from ..pessoas import models
from ..Livro import models

db_connection_str = settings.db_connection_str

engine = create_engine(
    db_connection_str,
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session
