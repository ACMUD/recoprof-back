from odmantic.bson import ObjectId
from pydantic import BaseModel
from validations.Values import FacultadesValidas

class ProfesorBase(BaseModel):
    id: ObjectId
    nombre: str
    facultades: list[FacultadesValidas]

class ProfesorAsignaturas(ProfesorBase):
    asignaturas: list[ObjectId]

class ComentarioBase(BaseModel):
    id: ObjectId
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    asignatura: ObjectId
    semestre: str

class AsignaturasBase(BaseModel):
    id: ObjectId
    nombre: str
    codigo: int

class Token(BaseModel):
    access_token: str
    token_type: str