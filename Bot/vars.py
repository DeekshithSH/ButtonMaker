from os import environ
from dotenv import load_dotenv
load_dotenv()

class Var:
    API_ID: int=int(environ.get("API_ID"))
    API_HASH: str=environ.get("API_HASH")
    BOT_TOKEN: str=environ.get("BOT_TOKEN")
    WORKER: int=int(environ.get("WORKER", 4))
    
