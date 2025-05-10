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

@router.get('/list', response_model = rb.PaginacionAsignaturasBase)
async def list_asignaturas(page: int = 0, limit: int = 10, name:str = '', facultad: FacultadesValidas = None):
    name = name.upper()
    args = [Asignatura, Asignatura.nombre.match("[A-z0-9 ]*"+name+"[A-z0-9 ]*"), Asignatura.facultades==facultad if facultad else {}]
    kwargs = {"skip":page*limit, "limit":limit}
    total = await Engine.count(*args)
    return {"contenido": await Engine.find(*args, **kwargs),
            "total" : total,
            "pagina": page,
            "total_paginas" : (total + limit - 1) // limit if limit > 0 else 1
            }

@router.get('/profes/{asignatura_id}', response_model=rb.PaginacionProfesorBase)
async def get_asignatura_profs(asignatura_id: ObjectId, page: int = 0, limit:int = 10):

    args = [Profesor, Profesor.asignaturas==asignatura_id]
    kwargs = {"skip":page*limit, "limit":limit}

    total = await Engine.count(*args)
    return {"contenido": await Engine.find(*args, **kwargs),
            "total": total,
            "pagina": page,
            "total_paginas": (total + limit - 1) // limit if limit > 0 else 1}