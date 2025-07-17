from dependencies.repository_access import get_profesor_repository
from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from db.models import Profesor
import responseBody as rb
from typing import Annotated
from .auth import access
from validations.Values import FacultadesValidas

router = APIRouter(
    tags=["profesor"],
    prefix="/api/profesor"
)



@router.get('/list', response_model = rb.PaginacionProfesor)
async def list_profesores(page: int = 0, limit: int = 10, name:str = '', facultad: FacultadesValidas = None, repo = Depends(get_profesor_repository)):
    name = name.upper()

    profesores = await repo.get_profesor_list(page, limit, name, facultad)
    total = await repo.count_profesor_list(name, facultad)
    
    return {"contenido":profesores,
            "total": total,
            "pagina": page,
            "total_paginas": (total + limit - 1) // limit if limit > 0 else 1}




@router.get('/{profesor_id}', response_model=rb.ProfesorConAsignatura)
async def get_profesor(profesor_id: ObjectId, repo = Depends(get_profesor_repository)):
    profesor = await repo.get_profesor_by_id(profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor not found")
    return profesor

@router.get('/puntaje/{profesor_id}', response_model=list[rb.NotasProcesadas])
async def get_profesor_score(profesor_id: ObjectId, repo = Depends(get_profesor_repository)):
    response = await repo.get_profesor_score(profesor_id)
    return response



@router.post('/create', response_model=Profesor)
async def create_profesor(profesor: Profesor, acc: Annotated[bool, Depends(access)], repo = Depends(get_profesor_repository)):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    profesor.nombre = profesor.nombre.upper()
    if not profesor.facultades:
        raise HTTPException(status_code=400, detail="Facultades cannot be empty")

    return await repo.create_profesor(profesor)


@router.delete('/delete/{profesor_id}')
async def delete_profesor(profesor_id: ObjectId, acc: Annotated[bool, Depends(access)], repo = Depends(get_profesor_repository)):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    result = await repo.delete_profesor(profesor_id)
    if not result:
        raise HTTPException(status_code=404, detail="Profesor not found")
    
    return {"status": "ok", "message": "Profesor deleted successfully"}
    