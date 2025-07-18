from fixtures import comentario_servicio, comentario_mock, nota_mock
import logging
import pytest

logging.basicConfig(level=logging.INFO)

@pytest.mark.asyncio
async def test_post_comment(comentario_servicio, comentario_mock):
    result = await comentario_servicio.post_comment(comentario_mock)
    logging.info(f"Post comment result: {result}")
    assert result is True

@pytest.mark.asyncio
async def test_get_comment(comentario_servicio, comentario_mock):
    comment_id = comentario_mock.id
    data = await comentario_servicio.get_comentario(comment_id)
    logging.info(f"Retrieved comment: {data}")
    assert data is not None
    assert data.id == comment_id

@pytest.mark.asyncio
async def test_delete_comment(comentario_servicio, comentario_mock):
    result = await comentario_servicio.delete_comment(comentario_mock.id)
    logging.info(f"Delete comment result: {result}")

    # Verify deletion
    data = await comentario_servicio.get_comentario(comentario_mock.id)
    assert data is None
    logging.info(f"Comment after deletion: {data}")
