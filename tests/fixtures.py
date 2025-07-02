from db.repository.profesor_repository import ProfesorRepository
from db.repository.asignaturas_repository import AsignaturasRepository
from odmantic import ObjectId
import pytest_asyncio
from db.models import Profesor, Asignatura
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