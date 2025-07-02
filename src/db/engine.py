# db/engine.py
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os

uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017") 

client = AsyncIOMotorClient(uri)
engine = AIOEngine(client, database="recoprof")

@asynccontextmanager
async def get_engine():
    '''
    For context manager usage and testing purposes.
    '''
    client = AsyncIOMotorClient(uri)
    engine = AIOEngine(client, database="recoprof")
    yield engine