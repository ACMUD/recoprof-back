from fixtures import profe_repo, profesor1_mock, profesor2_mock
import logging
import pytest


logging.basicConfig(level=logging.INFO)
    

@pytest.mark.asyncio
async def test_create_profesor(profe_repo, profesor1_mock, profesor2_mock):
    data = await profe_repo.create_profesor(profesor1_mock)
    logging.info(f"Created profesor: {data}")
    data = await profe_repo.create_profesor(profesor2_mock)
    logging.info(f"Created profesor: {data}")

@pytest.mark.asyncio
async def test_get_profesor_by_id(profe_repo, profesor1_mock):
    logging.info("Testing get_profesor_by_id with a valid ID")
    data = await profe_repo.get_profesor_by_id(profesor1_mock.id)
    logging.info(f"Retrieved data: {data}")

@pytest.mark.asyncio
async def test_get_profesor_list(profe_repo):
    logging.info("Testing get_profesor_list with default parameters")
    data = await profe_repo.get_profesor_list()
    logging.info(f"Retrieved data: {data}")
    count = await profe_repo.count_profesor_list()
    logging.info(f"Total count: {count}")

@pytest.mark.asyncio
async def test_get_profesor_score(profe_repo, profesor1_mock):
    logging.info("Testing get_profesor_score with a valid ID")
    data = await profe_repo.get_profesor_score(profesor1_mock.id)
    logging.info(f"Retrieved score data: {data}")

@pytest.mark.asyncio
async def test_delete_profesor(profe_repo, profesor1_mock):
    logging.info("Testing delete_profesor with a valid ID"+str(profesor1_mock.id))
    data = await profe_repo.delete_profesor(profesor1_mock.id)
    logging.info(f"Deleted profesor: {data}")