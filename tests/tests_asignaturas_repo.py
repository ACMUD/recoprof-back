from fixtures import asignatura_repo, asignatura_mock
import logging
import pytest


logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_create_asignatura(asignatura_repo, asignatura_mock):
    logging.info("Testing create_asignatura")
    data = await asignatura_repo.create_asignatura(asignatura_mock)
    logging.info(f"Created asignatura: {data}")

@pytest.mark.asyncio
async def test_list_asignaturas(asignatura_repo):
    asignaturas = await asignatura_repo.list_asignaturas()
    count = await asignatura_repo.count_asignaturas()
    logging.info(f"Asignaturas: {asignaturas}")
    logging.info(f"Total asignaturas: {count}")

@pytest.mark.asyncio
async def test_asignatura_profesores(asignatura_repo, asignatura_mock):
    asignatura_id = asignatura_mock.id

    data = await asignatura_repo.get_asignatura_profs(asignatura_id)
    count = await asignatura_repo.count_asignatura_profs(asignatura_id)

    logging.info(f"Profesores de la asignatura: {data}")
    logging.info(f"Total profesores de la asignatura: {count}")
    
