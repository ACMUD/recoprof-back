from odmantic.bson import ObjectId
from pydantic import BaseModel
from validations.Values import FacultadesValidas

class ProfesorBase(BaseModel):
    id: ObjectId
    nombre: str
    facultad: FacultadesValidas
    puntuacion: float
    clases: list[str]

class ComentarioBase(BaseModel):
    id: ObjectId
    comentario: str
    puntuacion: float = 0
    asignatura: str
    semestre: str

class Token(BaseModel):
    access_token: str
    token_type: str