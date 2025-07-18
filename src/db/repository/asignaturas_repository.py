from odmantic import AIOEngine
from db.models import Asignatura, Profesor
from typing import Optional
from validations.Values import FacultadesValidas


class AsignaturasRepository:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def get_asignatura_by_code(self, asignatura_code: str) -> Asignatura | None:
        asignatura = await self.engine.find_one(Asignatura, Asignatura.codigo == asignatura_code)
        return asignatura

    async def get_asignatura_by_id(self, asignatura_id: str) -> Asignatura | None:
        asignatura = await self.engine.find_one(Asignatura, Asignatura.id == asignatura_id)
        return asignatura

    async def create_asignatura(self, asignatura: Asignatura) -> Asignatura:
        asignatura.nombre = asignatura.nombre.upper()
        await self.engine.save(asignatura)
        return asignatura

    async def list_asignaturas(self, page: int = 0, limit: int = 10, name: str = '', facultad: Optional[FacultadesValidas] = None):
        name = name.upper()
        return await self.engine.find(Asignatura, Asignatura.nombre.match("[A-z0-9 ]*" + name + "[A-z0-9 ]*"), Asignatura.facultades == facultad if facultad else {}, skip = page * limit, limit = limit)

    async def count_asignaturas(self, name: str = '', facultad: Optional[FacultadesValidas] = None) -> int:
        name = name.upper()
        return await self.engine.count(Asignatura, Asignatura.nombre.match("[A-z0-9 ]*" + name + "[A-z0-9 ]*"), Asignatura.facultades == facultad if facultad else {})

    async def get_asignatura_profs(self, asignatura_id: str, page: int = 0, limit: int = 10) -> list[Profesor]:
        return await self.engine.find(Profesor, Profesor.asignaturas==asignatura_id, skip=page*limit, limit=limit)

    async def count_asignatura_profs(self, asignatura_id: str) -> int:
        return await self.engine.count(Profesor, Profesor.asignaturas==asignatura_id)
