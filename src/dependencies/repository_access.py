from db.engine import get_engine_context
from db.repository.profesor_repository import ProfesorRepository
from db.repository.asignaturas_repository import AsignaturasRepository
from db.repository.notas_repository import NotasRepository
from db.repository.comentarios_repository import ComentarioRepository

async def get_profesor_repository():
    async with get_engine_context() as engine:
        return ProfesorRepository(engine)

async def get_asignaturas_repository():
    async with get_engine_context() as engine:
        return AsignaturasRepository(engine)

async def get_notas_repository():
    async with get_engine_context() as engine:
        return NotasRepository(engine)

async def get_comentarios_repository():
    async with get_engine_context() as engine:
        return ComentarioRepository(engine)
