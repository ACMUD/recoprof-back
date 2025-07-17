from db.engine import get_engine
from services.comments_service import CommentsService

async def get_comments_service():
    engine = await get_engine()
    # Usar modo legacy con engine por simplicidad
    return CommentsService(comentarios_repo=None, engine=engine)