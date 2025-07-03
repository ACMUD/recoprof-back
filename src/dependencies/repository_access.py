from db.engine import engine
from db.repository.profesor_repository import ProfesorRepository
from db.repository.asignaturas_repository import AsignaturasRepository
from db.repository.notas_repository import NotasRepository
from db.repository.comentarios_repository import ComentarioRepository

def get_profesor_repository():
    return ProfesorRepository(engine)

def get_asignaturas_repository():
    return AsignaturasRepository(engine)

def get_notas_repository():
    return NotasRepository(engine)

def get_comentario_repository():
    return ComentarioRepository(engine)