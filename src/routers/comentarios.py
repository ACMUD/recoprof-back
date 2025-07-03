from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from db.models import Comentario
from responseBody import ComentarioBase
from typing import Annotated
from .auth import access
from dependencies.repository_access import get_comentario_repository
from dependencies.services_access import get_comments_service

router = APIRouter(
    tags=["comment"],
    prefix="/api/comment"
)

@router.get('/{profesor_id}', response_model=list[ComentarioBase])
async def get_profesor_comments(profesor_id: ObjectId, asignatura=None, page: int = 0, limit: int = 10, repo_comentario=Depends(get_comentario_repository)):
    return await repo_comentario.get_comments_by_profesor(profesor_id, asignatura, page, limit)


@router.post('/')
async def create_comment(comentario: Comentario, comment_service = Depends(get_comments_service)):
    """
    Crea un commentario para un profesor, si la asignatura no existe, se crea una nueva, y asi mismo actualiza el promedio.
    finalmente agrega el promedio al profesor.
    """
    value = await comment_service.post_comment(comentario)
    await comment_service.update_profesor_score(comentario.profesor)
    return value

@router.delete('/{comment_id}')
async def delete_comment(comment_id: ObjectId, acc: Annotated[bool, Depends(access)], comment_service = Depends(get_comments_service)):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    comment = await comment_service.get_comentario(comment_id)
    value = await comment_service.delete_comment(comment_id)
    await comment_service.update_profesor_score(comment.profesor)
    return value