import uvicorn
from fastapi import FastAPI

from core.db import settings
from core.models import HealthCheck
from core.db import engine, SQLModel
from router.endpoints import api_router

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)

SQLModel.metadata.create_all(engine)


@app.get('/', response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "nome": settings.project_name,
        "version": settings.version
    }


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
