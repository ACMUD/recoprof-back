from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import ObjectId
from db.models import Comentario
from responseBody import ComentarioBase
from schemas.comment_post import CommentPostSchema
from services.comments_service import CommentsService
from typing import Annotated, Literal
from .auth import access
from dependencies.repository_access import get_comentarios_repository
from dependencies.services_access import get_comments_service

router = APIRouter(
    tags=["comment"],
    prefix="/api/comment"
)

@router.get('/{profesor_id}', response_model=list[ComentarioBase])
async def get_profesor_comments(profesor_id: ObjectId, asignatura=None, page: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=20), repo_comentario=Depends(get_comentarios_repository)):
    return await repo_comentario.get_comments_by_profesor(profesor_id, asignatura, page, limit)


@router.post('/')
async def create_comment(comentario: CommentPostSchema, comment_service: CommentsService = Depends(get_comments_service)):
    """
    Crea un commentario para un profesor, y actualiza el promedio.
    """
    comentario_post: Comentario = Comentario(**comentario.dict())
    try:
        value: Comentario = await comment_service.post_comment(comentario_post)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return value
    #await comment_service.update_profesor_score(comentario.profesor)
    #return value

@router.delete('/{comment_id}')
async def delete_comment(comment_id: ObjectId, acc: Annotated[bool, Depends(access)], comment_service = Depends(get_comments_service)):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        value = await comment_service.delete_comment(comment_id)
        return value
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/votes/{comment_id}')
async def vote_comment(comment_id: ObjectId, vote: Literal["up", "down"], comment_service: CommentsService = Depends(get_comments_service)):
    try:
        value = await comment_service.vote_comment(comment_id, vote)
        return value
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
