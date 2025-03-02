from db.engine import Engine
from db.models import dbconfig
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from .auth import access

router = APIRouter(
    tags=["Admin"],
    prefix="/api"
)

@router.post('/configure')
async def configure(acc: Annotated[bool, Depends(access)]):
    """
    Utility endpoint to configure the database
    """
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await Engine.configure_database(dbconfig,update_existing_indexes=True)
