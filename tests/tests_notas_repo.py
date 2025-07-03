from fixtures import notas_repo, nota_mock
import logging
import pytest


logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_save_nota(notas_repo, nota_mock):
    data = await notas_repo.save_notas(nota_mock)
    logging.info(f"Saved nota: {data}")

@pytest.mark.asyncio
async def test_get_nota(notas_repo, nota_mock):
    nota_id = nota_mock.id
    data = await notas_repo.get_notas(nota_mock.asignatura, nota_mock.profesor)
    logging.info(f"Retrieved nota: {data}")
    assert data is not None
    assert data.id == nota_id

@pytest.mark.asyncio
async def test_delete_nota(notas_repo, nota_mock):
    value = await notas_repo.delete_notas(nota_mock.id)
    logging.info(f"Deleted nota: {value}")
    
    # Verify deletion
    data = await notas_repo.get_notas(nota_mock.asignatura, nota_mock.profesor)
    assert data is None
    logging.info(f"Nota after deletion: {data}")