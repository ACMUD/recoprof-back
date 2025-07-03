from odmantic import AIOEngine, ObjectId
from db.models import Comentario

class ComentarioRepository:
    def __init__(self, engine: AIOEngine):
        self.engine = engine
    
    async def create_comentario(self, comentario: Comentario) -> Comentario:
        return await self.engine.save(comentario)
    
    async def get_comentario(self, comentario_id: ObjectId) -> Comentario:
        return await self.engine.find_one(Comentario, Comentario.id == comentario_id)
        

    async def get_comments_by_profesor(self, profesor_id: ObjectId, asignatura: ObjectId = None, page: int = 0, limit: int = 10):
        query = [Comentario.profesor == profesor_id]
        if asignatura:
            query.append(Comentario.asignatura == asignatura)
        return await self.engine.find(Comentario, *query, skip=page * limit, limit=limit)
    
    async def delete_comentario(self, comentario_id: ObjectId) -> bool:
        comentario = await self.engine.find_one(Comentario, Comentario.id == comentario_id)
        if comentario:
            await self.engine.delete(comentario)
            return True
        return False
    
    async def count_comments(self, profesor_id: ObjectId, asignatura: ObjectId = None, semestre: tuple = None) -> int:
        query = [Comentario.profesor == profesor_id]
        if asignatura:
            query.append(Comentario.asignatura == asignatura)
        if semestre:
            query.append(Comentario.asignatura== semestre)
        return await self.engine.count(Comentario, *query)