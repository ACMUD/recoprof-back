from db.repository.profesor_repository import ProfesorRepository
from odmantic import ObjectId
import pytest_asyncio
from db.models import Profesor
from db.engine import get_engine
import pytest

@pytest_asyncio.fixture
async def profe_repo():
    async with get_engine() as engine:
        return ProfesorRepository(engine)
    
@pytest.fixture
def profesor_mock():
    return Profesor(**{
        "id": ObjectId('5f85f36d6dfecacc68428a46'),
        "nombre": "Juan Perez",
        "facultades": ["Ingenieria"],
        "asignaturas": []
    })