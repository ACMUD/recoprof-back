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

        profesor = await self.repo_profesor.get_profesor(comentario.profesor)
        if not profesor:
            raise ValueError("Profesor not found")
        if comentario.asignatura not in profesor.asignaturas:
            raise ValueError("Profesor does not teach this subject")

        return await self.repo_comentario.save(comentario)
