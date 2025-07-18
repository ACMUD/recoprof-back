from fastapi import APIRouter, HTTPException, Depends
from db.models import Asignatura
from typing import Annotated
from odmantic.bson import ObjectId
from dependencies.auth_dep import access
from dependencies.repository_access import get_asignaturas_repository

from validations.Values import FacultadesValidas

import responseBody as rb

router = APIRouter(
    tags=["asignatura"],
    prefix="/api/asignatura"
)


@router.post('/')
async def create_asisgnatura(asignatura: Asignatura, acc: Annotated[bool, Depends(access)], repo= Depends(get_asignaturas_repository)):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return await repo.create_asignatura(asignatura)

@router.get('/', response_model = rb.PaginacionAsignaturasBase)
async def list_asignaturas(page: int = 0, limit: int = 10, name:str = '', facultad: FacultadesValidas = None, repo= Depends(get_asignaturas_repository)):
    contenido = await repo.list_asignaturas(page, limit, name, facultad)
    total = await repo.count_asignaturas(name, facultad)
    return {"contenido": contenido,
            "total" : total,
            "pagina": page,
            "total_paginas" : (total + limit - 1) // limit if limit > 0 else 1
            }

@router.get('/{asignatura_id}', response_model=Asignatura)
async def get_asignatura_by_id(asignatura_id: ObjectId, repo= Depends(get_asignaturas_repository)):
    asignatura = await repo.get_asignatura_by_id(asignatura_id)
    if not asignatura:
        raise HTTPException(status_code=404, detail="Asignatura not found")
    return asignatura

@router.get('/profesores/{asignatura_id}', response_model=rb.PaginacionProfesorBase)
async def get_asignatura_profs(asignatura_id: ObjectId, page: int = 0, limit:int = 10, repo= Depends(get_asignaturas_repository)):
    contenido = await repo.get_asignatura_profs(asignatura_id, page, limit)
    total = await repo.count_asignatura_profs(asignatura_id)
    return {"contenido": contenido,
            "total": total,
            "pagina": page,
            "total_paginas": (total + limit - 1) // limit if limit > 0 else 1}
