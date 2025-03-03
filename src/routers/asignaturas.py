from db.engine import Engine
from fastapi import APIRouter, HTTPException, Depends
from db.models import Asignatura
from typing import Annotated
from .auth import access

router = APIRouter(
    tags=["asignatura"],
    prefix="/api/asignatura"
)


@router.post('/')
async def create_asisgnatura(asignatura: Asignatura, acc: Annotated[bool, Depends(access)]):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    asignatura.nombre = asignatura.nombre.upper()
    await Engine.save(asignatura)
    return asignatura

@router.get('/list')
async def list_asignaturas(page: int = 0, limit: int = 10):
    return await Engine.find(Asignatura, skip=page*limit, limit=limit)