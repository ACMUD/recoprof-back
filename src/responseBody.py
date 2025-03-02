from typing import Union
from odmantic.bson import ObjectId
from pydantic import BaseModel

class ClaseNombre(BaseModel):
    asignatura: str

class ProfesorBase(BaseModel):
    id: ObjectId
    nombres: str
    apellidos: str
    puntuacion: float
    clases: list[ClaseNombre]

class ComentarioBase(BaseModel):
    comentario: str
    puntuacion: float = 0
    asignatura: str
    semestre: str

class Token(BaseModel):
    access_token: str
    token_type: str