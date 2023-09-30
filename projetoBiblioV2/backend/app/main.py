import sys

sys.path.extend(['/home/jmrflora/repos/biblioteca-python/projetoBiblioV2/'])
import sqlmodel
import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

from backend.app import settings
from backend.app.schemas import models
from backend.app.schemas.models import HealthCheck
from backend.app.core.db import engine
from backend.app.router.endpoints import api_router

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

# SQLModel.metadata.create_all(engine)


app.include_router(api_router)


@app.get('/', response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "nome": settings.project_name,
        "version": settings.version
    }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
