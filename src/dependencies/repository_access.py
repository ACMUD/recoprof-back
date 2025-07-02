from db.engine import engine
from db.repository.profesor_repository import ProfesorRepository
from db.repository.asignaturas_repository import AsignaturasRepository

def get_profesor_repository():
    return ProfesorRepository(engine)

def get_asignaturas_repository():
    return AsignaturasRepository(engine)