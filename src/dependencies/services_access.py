from db.engine import get_engine_context
from services.comments_service import CommentsService
from db.repository.profesor_repository import ProfesorRepository
from db.repository.comentarios_repository import ComentarioRepository
from db.repository.notas_repository import NotasRepository

async def get_comments_service():
    async with get_engine_context() as engine:
        comentarios_repo: ComentarioRepository = ComentarioRepository(engine)
        repo_notas: NotasRepository = NotasRepository(engine)
        repo_profesor: ProfesorRepository = ProfesorRepository(engine)
        return CommentsService(comentarios_repo=comentarios_repo, repo_notas=repo_notas, repo_profesor=repo_profesor)
