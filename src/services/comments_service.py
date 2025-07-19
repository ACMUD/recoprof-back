from odmantic import ObjectId
from db.repository.profesor_repository import ProfesorRepository
from db.repository.comentarios_repository import ComentarioRepository
from db.repository.notas_repository import NotasRepository
from db.models import Notas, Puntuacion, Comentario, Profesor

class CommentsService:
    def __init__(self, comentarios_repo: ComentarioRepository, repo_notas: NotasRepository, repo_profesor: ProfesorRepository) -> None:
        self.repo_comentario = comentarios_repo
        self.repo_notas = repo_notas
        self.repo_profesor = repo_profesor

    async def get_comentario(self, comentario_id):
        return await self.repo_comentario.get_comentario(comentario_id)

    async def post_comment(self, comentario: Comentario):

        profesor: Profesor | None = await self.repo_profesor.get_profesor(comentario.profesor)
        if not profesor:
            raise ValueError("Profesor not found")
        if comentario.asignatura not in profesor.asignaturas:
            raise ValueError("Profesor does not teach this subject")

        comment: Comentario = await self.repo_comentario.save(comentario)

        puntuacion: Puntuacion = Puntuacion(valor=comentario.puntuacion, cantidad = 1, semestre=comentario.semestre)

        await self.update_profesor_score(profesor.id, comentario.asignatura, puntuacion)
        return comment

    async def delete_comment(self, comment_id: ObjectId):
        comment: Comentario | None = await self.repo_comentario.get_comentario(comment_id)
        if not comment:
            raise ValueError("Comment not found")
        puntuacion: Puntuacion = Puntuacion(valor=-comment.puntuacion, cantidad=-1, semestre=comment.semestre)
        await self.update_profesor_score(comment.profesor, comment.asignatura, puntuacion)
        return await self.repo_comentario.delete_comentario(comment_id)

    async def update_profesor_score(self, profesor_id: ObjectId, asignatura_id: ObjectId, puntuacion: Puntuacion):
        notas: Notas | None = await self.repo_notas.get_notas(asignatura_id, profesor_id)
        if not notas:
            notas = Notas(asignatura=asignatura_id, profesor=profesor_id, puntuaciones=[puntuacion])
            return await self.repo_notas.save_notas(notas)

        if puntuacion.semestre not in [p.semestre for p in notas.puntuaciones]:
            notas.puntuaciones.append(puntuacion)
            return await self.repo_notas.save_notas(notas)

        for existing_puntuacion in notas.puntuaciones:
            if existing_puntuacion.semestre == puntuacion.semestre:
                existing_puntuacion.valor = (existing_puntuacion.valor*existing_puntuacion.cantidad + puntuacion.valor)
                divisor: int = (existing_puntuacion.cantidad + puntuacion.cantidad)
                if divisor > 0:
                    existing_puntuacion.valor /= divisor
                    existing_puntuacion.cantidad += puntuacion.cantidad
                    break
                notas.puntuaciones.remove(existing_puntuacion)

        if len(notas.puntuaciones) == 0:
            await self.repo_notas.delete_notas(notas.id)
            return

        return await self.repo_notas.save_notas(notas)
