from db.repository.profesor_repository import ProfesorRepository
from db.repository.comentarios_repository import ComentarioRepository
from db.repository.notas_repository import NotasRepository
from db.models import Notas, Puntuacion

class Comments_service:
    def __init__(self, engine):
        self.repo_comentario = ComentarioRepository(engine)
        self.repo_notas = NotasRepository(engine)
        self.repo_profesor = ProfesorRepository(engine)
    
    async def get_comentario(self, comentario_id):
        return await self.repo_comentario.get_comentario(comentario_id)
    
    async def post_comment(self, comentario):
        notas = await self.repo_notas.get_notas(comentario.asignatura, comentario.profesor)
        profesor = await self.repo_profesor.get_profesor(comentario.profesor)

        if not notas:
            notas = Notas(asignatura=comentario.asignatura, profesor=comentario.profesor, puntuaciones=[])
            profesor.asignaturas.append(comentario.asignatura)

        for p in notas.puntuaciones:
            if p.semestre == comentario.semestre:
                p.cantidad += 1
                p.valor = (p.valor*(p.cantidad-1) + comentario.puntuacion)/p.cantidad
                break
        else:
            
            puntuacion = Puntuacion(cantidad=1, valor=comentario.puntuacion, semestre=comentario.semestre)
            notas.puntuaciones.append(puntuacion)

        await self.repo_notas.save_notas(notas)
        await self.repo_comentario.create_comentario(comentario)
        return True
        
    async def delete_comment(self, comment_id):
        comment = await self.repo_comentario.get_comentario(comment_id)
        if not comment:
            return False
        
        notas = await self.repo_notas.get_notas(comment.asignatura, comment.profesor)
        if not notas:
            return False
        
        for p in notas.puntuaciones:
            if p.semestre == comment.semestre:
                p.cantidad -= 1
                if p.cantidad > 0:
                    p.valor = (p.valor*(p.cantidad+1) - comment.puntuacion)/p.cantidad
                else:
                    notas.puntuaciones.remove(p)
                break

        await self.repo_notas.save_notas(notas)
        return await self.repo_comentario.delete_comentario(comment_id)

    async def update_profesor_score(self, profesor_id):
        profesor = await self.repo_profesor.get_profesor(profesor_id)
        try:
            prom = await self.repo_profesor.get_promedio(profesor_id)
            profesor.puntuacion = prom[0]
        except Exception as e:
            print('No fue posible actualizar el promedio', e)

        await self.repo_profesor.create_profesor(profesor)
        return {"status": "ok"}