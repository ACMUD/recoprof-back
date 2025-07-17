from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import profs, admin, auth, asignaturas, comentarios
from db.engine import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación FastAPI.
    Inicializa la BD al inicio y la cierra al final.
    Optimizado para entornos serverless.
    """
    # Startup
    try:
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        # En serverless, es mejor continuar y manejar errores por endpoint
    
    yield
    
    # Shutdown
    try:
        await close_db()
        print("Database connection closed")
    except Exception as e:
        print(f"Error closing database: {e}")
        # En serverless, ignorar errores de cierre

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin)
app.include_router(profs)
app.include_router(comentarios)
app.include_router(asignaturas)
app.include_router(auth)

@app.get("/health")
async def health_check():
    return {"status": "ok"}