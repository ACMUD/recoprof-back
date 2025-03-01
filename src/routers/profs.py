from db.engine import Engine
from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from db.models import Profesor, ProfesorBasic

router = APIRouter(
    tags=["profesor"],
    prefix="/api/profesor"
)

@router.get('/list', response_model=list[ProfesorBasic])
async def list_profesores(page: int = 0, limit: int = 10):
    return await Engine.find(Profesor, skip=page*limit, limit=limit)

@router.get('/{profesor_id}', response_model=Profesor)
async def get_profesor(profesor_id: ObjectId):
    try:
        response = await Engine.find_one(Profesor, Profesor.id==profesor_id)
    except:
        HTTPException(status_code=404, detail="not found")
    return response

@router.post('/create', response_model=Profesor)
async def create_profesor(profesor: Profesor):
    profesor.nombres = profesor.nombres.upper()
    profesor.apellidos = profesor.apellidos.upper()
    return await Engine.save(profesor)