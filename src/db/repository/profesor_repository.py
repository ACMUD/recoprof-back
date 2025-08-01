from odmantic import AIOEngine
from db.models import Profesor, Notas
from db.pipelines import paginacion, match, LOOKUP_PIPE, NOTAS, NOTAS_PROMEDIO, PROMEDIO_GLOBAL
from validations.Values import FacultadesValidas
from typing import Optional

class ProfesorRepository:
    def __init__(self, engine: AIOEngine):
        self.engine = engine

    async def get_profesor(self, profesor_id) -> Profesor | None:
        """
        Obtiene la entidad Profesor por su ID.
        """
        return await self.engine.find_one(Profesor, Profesor.id == profesor_id)

    async def get_profesor_by_id(self, profesor_id):
        pipeline = []
        pipeline.extend(match("_id", profesor_id, regex=False))
        pipeline.extend(paginacion(0, 1))
        pipeline.extend(LOOKUP_PIPE)

        collection = self.engine.get_collection(Profesor)
        profesor = await collection.aggregate(pipeline).to_list(length=None)

        if len(profesor) == 0:
            return None
        return profesor[0]

    async def get_profesor_list(self, page: int = 0, limit: int = 10, name: str = '', facultad: FacultadesValidas = None):
        name = name.upper()
        pipeline = []
        pipeline.extend(match("nombre", name))
        if facultad:
            pipeline.extend(match("facultades", facultad))
        pipeline.extend(paginacion(page, limit))
        pipeline.extend(LOOKUP_PIPE)

        collection = self.engine.get_collection(Profesor)
        profesores = await collection.aggregate(pipeline).to_list(length=None)

        return profesores

    async def count_profesor_list(self, name: str = '', facultad: Optional[FacultadesValidas] = None):
        name = name.upper()
        total: int = await self.engine.count(Profesor, Profesor.nombre.match("[A-z0-9 ]*"+name+"[A-z0-9 ]*"),Profesor.facultades == facultad if facultad else {})
        return total

    async def create_profesor(self, profesor: Profesor):
        profesor.id = None
        profesor.nombre = profesor.nombre.upper()
        return await self.engine.save(profesor)

    async def save(self, profesor: Profesor):
        """
        Funcion atajo para guardar un profesor
        """
        return await self.engine.save(profesor)

    async def update_profesor(self, profesor: Profesor):
        if not profesor.id:
            raise ValueError("Profesor ID is required for update")
        profesordb: Profesor | None = await self.get_profesor(profesor.id)
        if not profesordb:
            raise ValueError("Profesor not found")
        profesordb.model_update(profesor)
        profesordb.nombre = profesor.nombre.upper()

        return await self.engine.save(profesor)

    async def delete_profesor(self, profesor_id):
        try:
            #await self.engine.remove(Notas, Notas.profesor == profesor_id)
            #await self.engine.remove(Asignatura, Asignatura.profesor == profesor_id)
            await self.engine.remove(Profesor, Profesor.id == profesor_id)
            return True
        except:
            return False

    async def get_profesor_score(self, profesor_id) -> int:
        """
        Retorna el promedio de todas las notas dadas al profesor.
        """
        pipeline = []
        pipeline.extend(match("profesor", profesor_id, regex=False))
        pipeline.extend(PROMEDIO_GLOBAL)

        collection = self.engine.get_collection(Notas)
        response = await collection.aggregate(pipeline).to_list(length=None)
        if len(response) == 0:
            return -1
        return response[0]["promedio"]

    async def get_promedio(self, profesor_id) -> list:
        """
        Retorna el promedio de todas las notas dadas al profesor por semestre.
        """
        pipeline = []
        pipeline.extend(match("profesor", profesor_id, False))
        pipeline.extend(NOTAS_PROMEDIO)

        collection = self.engine.get_collection(Notas)

        return await collection.aggregate(pipeline).to_list(length=None)
