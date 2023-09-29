import sys
sys.path.extend(['/home/jmrflora/repos/biblioteca-python/projetoBiblioV2/'])
from os import getenv


from dotenv import load_dotenv


from backend.app.core.config import Settings


load_dotenv(getenv("ENV_FILE"))
settings = Settings()
