from db.engine import Engine
from fastapi import APIRouter, HTTPException, Depends
from odmantic import ObjectId
from db.models import Comentario, Notas, Puntuacion, Profesor
from responseBody import ComentarioBase
from typing import Annotated
from .auth import access

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
    if 5< comentario.puntuacion or comentario.puntuacion < 0:
        raise HTTPException(status_code=400, detail="Puntuacion invalida")

    notas = await Engine.find_one(Notas, Notas.asignatura==comentario.asignatura, Notas.profesor==comentario.profesor)
    if not notas:
        profesor = await Engine.find_one(Profesor, Profesor.id==comentario.profesor)
        notas = Notas(asignatura=comentario.asignatura, profesor=comentario.profesor, puntuaciones=[])
        profesor.asignaturas.append(comentario.asignatura)
        await Engine.save(profesor)
        
    cantidad = await Engine.count(Comentario, Comentario.profesor==comentario.profesor, Comentario.asignatura==comentario.asignatura, Comentario.semestre==comentario.semestre)

    for p in notas.puntuaciones:
        if p.semestre == comentario.semestre:
            cantidad += 1
            p.valor = (p.valor*(cantidad-1) + comentario.puntuacion)/cantidad
            break
    else:
        puntuacion = Puntuacion(cantidad=1, valor=comentario.puntuacion, semestre=comentario.semestre)
        notas.puntuaciones.append(puntuacion)
    
    await Engine.save(notas)
    await Engine.save(comentario)
    return {"status": "ok"}


@router.delete('/{comment_id}')
async def create_comment(comment_id: ObjectId, acc: Annotated[bool, Depends(access)]):
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    comment = await Engine.find_one(Comentario, Comentario.id==comment_id)
    notas = await Engine.find_one(Notas,
                                  Notas.asignatura==comment.asignatura,
                                  Notas.profesor==comment.profesor)
    
    for p in notas.puntuaciones:
        if p.semestre == comment.semestre:
            p.cantidad -= 1
            p.valor = (p.valor*(p.cantidad+1) - comment.puntuacion)/(p.cantidad)
            break
    
    r = await Engine.remove(Comentario, Comentario.id==comment_id)
    await Engine.save(notas)
    return r
