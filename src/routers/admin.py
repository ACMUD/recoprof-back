from db.engine import Engine
from db.models import dbconfig
from fastapi import APIRouter
import os

ADMINPASS = os.environ.get('ADMIN_PSSWD') or os.urandom(16).hex()

router = APIRouter(
    tags=["Admin"],
    prefix="/api"
)

@router.post('/configure')
async def configure(passwd: str):
    """
    Utility endpoint to configure the database
    """
    if ADMINPASS == passwd:
        await Engine.configure_database(dbconfig,update_existing_indexes=True)
