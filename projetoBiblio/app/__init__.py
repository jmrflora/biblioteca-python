from os import getenv


from dotenv import load_dotenv


from projetoBiblio.app.core.config import Settings


load_dotenv(getenv("ENV_FILE"))
settings = Settings()
