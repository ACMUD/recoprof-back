from odmantic import AIOEngine
from db.models import Notas
from odmantic import ObjectId

class NotasRepository:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def get_notas(self, asignatura: ObjectId, profesor_id: ObjectId)->Notas:
        return await self.engine.find_one(Notas, Notas.asignatura == asignatura, Notas.profesor == profesor_id)

    async def save_notas(self, notas: Notas) -> Notas:
        return await self.engine.save(notas)

    async def delete_notas(self, notas_id: ObjectId) -> bool:
        try:
            await self.engine.remove(Notas, notas_id==Notas.id)
            return True
        except Exception as e:
            print(f"Error deleting notas: {e}")
            return False
