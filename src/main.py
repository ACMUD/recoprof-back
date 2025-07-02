from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import profs, admin, auth, asignaturas


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin)
app.include_router(profs)
#app.include_router(comentarios)
app.include_router(asignaturas)
app.include_router(auth)

@app.get("/health")
async def health_check():
    return {"status": "ok"}