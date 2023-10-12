from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    project_name: str
    version: str

    # Database
    db_connection_str: str