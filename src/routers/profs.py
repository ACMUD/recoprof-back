from db.engine import Engine
from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from db.models import Profesor, Comentario, Notas
from responseBody import ProfesorBase
from typing import Annotated
from .auth import access

router = APIRouter(
    tags=["profesor"],
    prefix="/api/profesor"
)

@router.get('/list', response_model=list[ProfesorBase])
async def list_profesores(page: int = 0, limit: int = 10):
    profesor = await Engine.find(Profesor, skip=page*limit, limit=limit)
    return profesor

@router.get('/{profesor_id}', response_model=Profesor)
async def get_profesor(profesor_id: ObjectId):
    try:
        response = await Engine.find_one(Profesor, Profesor.id==profesor_id)

    except:
        HTTPException(status_code=404, detail="not found")
    return response

@router.get('/puntaje/{profesor_id}', response_model=Profesor)
async def get_profesor(profesor_id: ObjectId):
    try:
        response = await Engine.find(Notas, Notas.profesor==profesor_id)
    except:
        HTTPException(status_code=404, detail="not found")
    return response

@router.post('/create', response_model=Profesor)
async def create_profesor(profesor: Profesor, acc: Annotated[bool, Depends(access)]):
    profesor.nombres = profesor.nombres.upper()
    profesor.apellidos = profesor.apellidos.upper()
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
        HTTPException(status_code=404, detail="not found")
    return {"status": "ok"}