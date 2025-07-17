from db.repository.profesor_repository import ProfesorRepository
from db.repository.comentarios_repository import ComentariosRepository
from db.repository.notas_repository import NotasRepository
from db.models import Notas, Puntuacion

class CommentsService:
    def __init__(self, comentarios_repo: ComentariosRepository, engine=None):
        if engine is not None:
            # Modo legacy para compatibilidad
            self.repo_comentario = ComentariosRepository(engine)
            self.repo_notas = NotasRepository(engine)
            self.repo_profesor = ProfesorRepository(engine)
        else:
            # Nuevo modo usando repository injection
            self.repo_comentario = comentarios_repo
            # Estos necesitarán ser inyectados por separado o refactorizados
            self.repo_notas = None
            self.repo_profesor = None
    
    async def get_comentario(self, comentario_id):
        return await self.repo_comentario.get_comentario(comentario_id)
    
    async def post_comment(self, comentario):
        if not self.repo_notas or not self.repo_profesor:
            raise RuntimeError("NotasRepository and ProfesorRepository must be provided")
            
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

    async def delete_comment(self, comentario_id):
        return await self.repo_comentario.delete_comentario(comentario_id)

    async def update_profesor_score(self, profesor_id):
        if not self.repo_profesor:
            raise RuntimeError("ProfesorRepository must be provided")
        return await self.repo_profesor.update_profesor_score(profesor_id)