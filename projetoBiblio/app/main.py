import uvicorn
from fastapi import FastAPI

from projetoBiblio.app import settings
from core.models import HealthCheck

app = FastAPI(
    title=settings.project_name,
    version=settings.version
)


@app.get('/', response_model=HealthCheck, tags=["status"])
async def health_check():
    return {
        "nome": settings.project_name,
        "version": settings.version
    }


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
