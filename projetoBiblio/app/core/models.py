from pydantic import BaseModel


class HealthCheck(BaseModel):
    nome: str
    version: str
