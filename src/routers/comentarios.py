from db.engine import Engine
from fastapi import APIRouter, HTTPException
from odmantic import ObjectId
from db.models import Comentario, ComentarioBase


router = APIRouter(
    tags=["comment"],
    prefix="/api/comment"
)

@router.get('/{profesor_id}', response_model=list[ComentarioBase])
async def get_profesor_comments(profesor_id: ObjectId, asignatura=None, page: int = 0, limit: int = 10):
    consulta = [Comentario.profesor==profesor_id]
    if asignatura:
        consulta.append(Comentario.asignatura==asignatura)
    response = await Engine.find(Comentario, *consulta, skip=page*limit, limit=limit)
    return response

@router.post('/')
async def create_comment(comentario: Comentario):
    if comentario.puntuacion < 0 or comentario.puntuacion > 5:
        raise HTTPException(status_code=400, detail="Puntuacion invalida")
    r = await Engine.save(comentario)
    return comentario
