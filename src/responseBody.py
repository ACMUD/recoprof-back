from odmantic.bson import ObjectId
from pydantic import BaseModel
from validations.Values import FacultadesValidas

class ProfesorBase(BaseModel):
    id: ObjectId
    nombre: str
    facultades: list[FacultadesValidas]

class ProfesorAsignaturas(ProfesorBase):
    asignaturas: list[ObjectId]

class Asignatura(BaseModel):
    id: ObjectId
    nombre: str

class ProfesorPorFacultad(BaseModel):
    id: ObjectId
    nombre: str
    asignaturas_nombre: list[Asignatura] =[]

class ComentarioBase(BaseModel):
    id: ObjectId
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    asignatura: ObjectId
    semestre: str

class AsignaturasBase(Asignatura):
    codigo: int

class Token(BaseModel):
    access_token: str
    token_type: str