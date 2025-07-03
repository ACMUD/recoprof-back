from fixtures import comentario_repo, comentario_mock
import logging
import pytest


logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_create_comentario(comentario_repo, comentario_mock):
    data = await comentario_repo.create_comentario(comentario_mock)
    logging.info(f"Created comentario: {data}")

@pytest.mark.asyncio
async def test_get_comentario(comentario_repo, comentario_mock):
    comentario_id = comentario_mock.id
    data = await comentario_repo.get_comentario(comentario_id)
    logging.info(f"Retrieved comentario: {data}")

@pytest.mark.asyncio
async def test_get_comments_by_profesor(comentario_repo, comentario_mock):
    profesor_id = comentario_mock.profesor
    data = await comentario_repo.get_comments_by_profesor(profesor_id)
    logging.info(f"Comments for profesor {profesor_id}: {data}")

@pytest.mark.asyncio
async def count_comments(comentario_repo, comentario_mock):
    profesor_id = comentario_mock.profesor
    count = await comentario_repo.count_comments(profesor_id)
    logging.info(f"Total comments for profesor {profesor_id}: {count}")

@pytest.mark.asyncio
async def test_delete_comentario(comentario_repo, comentario_mock):
    comentario_id = comentario_mock.id
    value = await comentario_repo.delete_comentario(comentario_id)
    logging.info(f"Deleted comentario: {value}")
    
    # Verify deletion
    data = await comentario_repo.get_comentario(comentario_id)