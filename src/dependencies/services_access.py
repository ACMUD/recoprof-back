from db.engine import engine
from services.comments_service import Comments_service

def get_comments_service():
    return Comments_service(engine)