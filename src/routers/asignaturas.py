from db.engine import Engine
from fastapi import APIRouter, HTTPException, Depends
from db.models import Asignatura, Profesor
from typing import Annotated
from odmantic.bson import ObjectId
from .auth import access

from validations.Values import FacultadesValidas

import responseBody as rb

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

@router.get('/profes/{asignatura_id}', response_model=list[rb.ProfesorBase])
async def get_asignatura_profs(asignatura_id: ObjectId):
    return await Engine.find(Profesor, {"asignaturas": {"$in": [asignatura_id]}})

@router.get('/facultad/{facultad}')
async def get_asignatura_facultad(facultad: FacultadesValidas, page: int = 0, limit: int = 10):
     # Contar el total de asignaturas que coinciden con el filtro
    total = await Engine.count(Asignatura, Asignatura.facultades == facultad)
    
    # Obtener las asignaturas con paginación y ordenación
    asignaturas = await Engine.find(
        Asignatura, 
        Asignatura.facultades == facultad,
        skip=page*limit,
        limit=limit
    )
    
    # Calcular metadatos de paginación
    total_paginas = (total + limit - 1) // limit if limit > 0 else 1
    
    asignaturas_simplificadas = [
        rb.AsignaturasBase(**asignatura.model_dump())
        for asignatura in asignaturas
    ]

    return {
        "asignaturas": asignaturas_simplificadas,
        "total": total,
        "total_paginas": total_paginas
    }
