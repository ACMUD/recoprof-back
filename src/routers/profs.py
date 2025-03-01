from db.engine import Engine
from db.models import dbconfig
from fastapi import APIRouter
from odmantic import ObjectId
from db.models import Profesor, ProfesorBasic
import os

router = APIRouter(
    tags=["profesor"],
    prefix="/api/profesor"
)

@router.get('/list', response_model=list[ProfesorBasic])
async def list_profesores(page: int = 0, limit: int = 10):
    return await Engine.find(Profesor, skip=page*limit, limit=limit)

@router.get('/{profesor_id}', response_model=Profesor)
async def get_profesor(profesor_id: ObjectId):
    return await Engine.find_one(Profesor, Profesor.id==profesor_id)

@router.post('/create', response_model=Profesor)
async def create_profesor(profesor: Profesor):
    return await Engine.save(profesor)