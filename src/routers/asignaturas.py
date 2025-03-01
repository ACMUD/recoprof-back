from db.engine import Engine
from fastapi import APIRouter, HTTPException
from db.models import Asignatura

router = APIRouter(
    tags=["asignatura"],
    prefix="/api/asignatura"
)


@router.post('/')
async def create_asisgnatura(asignatura: Asignatura):
    asignatura.nombre = asignatura.nombre.upper()
    await Engine.save(asignatura)
    return asignatura

@router.get('/list')
async def list_asignaturas(page: int = 0, limit: int = 10):
    return await Engine.find(Asignatura, skip=page*limit, limit=limit)