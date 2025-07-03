from db.repository.profesor_repository import ProfesorRepository
from db.repository.asignaturas_repository import AsignaturasRepository
from db.repository.comentarios_repository import ComentarioRepository
from db.repository.notas_repository import NotasRepository
from services.comments_service import Comments_service
from odmantic import ObjectId
import pytest_asyncio
from db.models import Profesor, Asignatura, Comentario, Notas
from db.engine import get_engine
import pytest

@pytest_asyncio.fixture
async def profe_repo():
    async with get_engine() as engine:
        return ProfesorRepository(engine)
    
@pytest_asyncio.fixture
async def asignatura_repo():
    async with get_engine() as engine:
        return AsignaturasRepository(engine)
    
@pytest_asyncio.fixture
async def notas_repo():
    async with get_engine() as engine:
        return NotasRepository(engine)
    
@pytest_asyncio.fixture
async def comentario_repo():
    async with get_engine() as engine:
        return ComentarioRepository(engine)
    
@pytest_asyncio.fixture
async def comentario_servicio():
    async with get_engine() as engine:
        return Comments_service(engine)
    
@pytest.fixture
def profesor1_mock():
    return Profesor(**{
        "id": ObjectId('5f85f36d6dfecacc68428a46'),
        "nombre": "Juan Perez",
        "facultades": ["Ingenieria"],
        "asignaturas": [ObjectId('67c67dc2b7bf4ad3f1153f03')]
    })

@pytest.fixture
def profesor2_mock():
    return Profesor(**{
        "id": ObjectId('5f85f36d6dfecacc68428a47'),
        "nombre": "Juan Perez",
        "facultades": ["Ingenieria"],
        "asignaturas": [ObjectId('67c67dc2b7bf4ad3f1153f03')]
    })

@pytest.fixture
def asignatura_mock():
    return Asignatura(
        **{
            "id":ObjectId('67c67dc2b7bf4ad3f1153f03'),
            "nombre":"PROGRAMACION ORIENTADA A OBJETOS",
            "facultades":["Ingenieria"],
            "codigo": 10
        }
    )

@pytest.fixture
def comentario_mock():
    return Comentario(**{
        "id": ObjectId('5f85f36d6dfecacc68428a48'),
        "comentario": "Comentario de prueba",
        "puntuacion": 5,
        "profesor": ObjectId('5f85f36d6dfecacc68428a47'),
        "asignatura": ObjectId('67c67dc2b7bf4ad3f1153f03'),
        "semestre": (2021,2),
    })

@pytest.fixture
def nota_mock():
    return Notas(**{
        "id": ObjectId('5f85f36d6dfecacc68428a48'),
        "profesor": ObjectId('5f85f36d6dfecacc68428a47'),
        "asignatura": ObjectId('67c67dc2b7bf4ad3f1153f03'),
        "puntuaciones": []
    })