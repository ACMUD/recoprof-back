# db/engine.py
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
import asyncio
from typing import Optional
from dotenv import load_dotenv
load_dotenv()

uri: str = os.environ.get("MONGO_URI", "mongodb://localhost:27017")

# Variable global para almacenar el engine actual
_engine: Optional[AIOEngine] = None
_client: Optional[AsyncIOMotorClient] = None

async def init_db():
    """Inicializa la conexión a la base de datos"""
    global _engine, _client
    if _engine is None:
        _client = AsyncIOMotorClient(uri)
        _engine = AIOEngine(_client, database="recoprof")
    return _engine

async def close_db():
    """Cierra la conexión a la base de datos"""
    global _engine, _client
    if _client:
        try:
            _client.close()
        except Exception:
            pass  # Ignorar errores al cerrar en serverless
    _engine = None
    _client = None

def get_engine() -> AIOEngine:
    """Obtiene la instancia actual del engine"""
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _engine

@asynccontextmanager
async def get_engine_context():
    """
    Context manager para pruebas y casos especiales.
    Crea una conexión temporal que se cierra automáticamente.
    """
    client: AsyncIOMotorClient = AsyncIOMotorClient(uri)
    engine: AIOEngine = AIOEngine(client, database="recoprof")
    try:
        yield engine
    finally:
        pass
