from db.engine import Engine
from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from db.models import Profesor, Comentario, Notas
import responseBody as rb
from typing import Annotated
from .auth import access
from validations.Values import FacultadesValidas

from utils.pipelines import paginacion, match, match_non_regex, LOOKUP_PIPE, NOTAS

router = APIRouter(
    tags=["profesor"],
    prefix="/api/profesor"
)



@router.get('/list', response_model = rb.PaginacionProfesor)
async def list_profesores(page: int = 0, limit: int = 10, name:str = '', facultad: FacultadesValidas = None):
    name = name.upper()

    total = await Engine.count(Profesor, Profesor.nombre.match("[A-z0-9 ]*"+name+"[A-z0-9 ]*"),Profesor.facultades == facultad if facultad else {})
    pipeline = []
    pipeline.extend(match("nombre", name))
    if facultad:
        pipeline.extend(match("facultades", facultad))
    pipeline.extend(paginacion(page, limit))
    pipeline.extend(LOOKUP_PIPE)
    

    collection = Engine.get_collection(Profesor)
    profesores = await collection.aggregate(pipeline).to_list(length=None)

    return {"contenido":profesores,
            "total": total,
            "pagina": page,
            "total_paginas": (total + limit - 1) // limit if limit > 0 else 1}




@router.get('/{profesor_id}', response_model=rb.ProfesorConAsignatura)
async def get_profesor(profesor_id: ObjectId):

    pipeline = []
    pipeline.extend(match_non_regex("_id", profesor_id))
    pipeline.extend(paginacion(0,1))
    pipeline.extend(LOOKUP_PIPE)
    

    collection = Engine.get_collection(Profesor)
    profesor = await collection.aggregate(pipeline).to_list(length=None)

    if len(profesor) == 0:
        raise HTTPException(status_code=404, detail="not found")
    return profesor[0]



@router.get('/puntaje/{profesor_id}', response_model=list[rb.NotasProcesadas])
async def get_profesor(profesor_id: ObjectId):
    pipeline = []
    pipeline.extend(match_non_regex("profesor", profesor_id))
    pipeline.extend(NOTAS)


    collection = Engine.get_collection(Notas)
    response = await collection.aggregate(pipeline).to_list(length=None)
    return response



@router.post('/create', response_model=Profesor)
async def create_profesor(profesor: Profesor, acc: Annotated[bool, Depends(access)]):
    profesor.nombre = profesor.nombre.upper()
    return await Engine.save(profesor)



@router.delete('/delete/{profesor_id}')
async def delete_profesor(profesor_id: ObjectId, acc: Annotated[bool, Depends(access)]):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        await Engine.remove(Profesor, Profesor.id==profesor_id)
        await Engine.remove(Comentario, Comentario.profesor==profesor_id)
        await Engine.remove(Notas, Notas.profesor==profesor_id)
    except:
        raise HTTPException(status_code=404, detail="not found")
    return {"status": "ok"}