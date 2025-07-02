from db.engine import engine
from db.repository.profesor_repository import ProfesorRepository

def get_profesor_repository():
    return ProfesorRepository(engine)