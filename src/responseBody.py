from odmantic.bson import ObjectId
from pydantic import BaseModel


class ProfesorBase(BaseModel):
    id: ObjectId
    nombres: str
    apellidos: str
    puntuacion: float
    asignaturas: list[str]

class ComentarioBase(BaseModel):
    id: ObjectId
    comentario: str
    puntuacion: float = 0
    asignatura: str
    semestre: str

class Token(BaseModel):
    access_token: str
    token_type: str