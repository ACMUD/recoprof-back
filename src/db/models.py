from odmantic import Model, Index, EmbeddedModel
from odmantic.bson import ObjectId
from validations.Values import FacultadesValidas

from pydantic import BaseModel

#database
class Clase(EmbeddedModel):
    asignatura: str
    puntuacion: float
    semestre: str

class Profesor(Model):
    nombres: str
    apellidos: str
    facultad: FacultadesValidas
    puntuacion: float = 0
    clases: list[Clase] = []
    
    model_config = {
        "indexes": lambda: [
            Index(Profesor.apellidos, name="profesor_apellidos")
        ]
    }

class Asignatura(Model):
    nombre: str
    codigo: str

    model_config = {
        "indexes": lambda: [
            Index(Asignatura.codigo, name="asignatura_codigo")
        ]
    }

class Comentario(Model):
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    asignatura: str
    semestre: str
    model_config = {
        "indexes": lambda: [
            Index(Comentario.profesor, name="comentario profesor"),
            Index(Comentario.semestre, name="comentario semestre")
        ]
    }

dbconfig = [Profesor, Asignatura, Comentario]



# RESPONSES

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