from odmantic import Model, Index, EmbeddedModel
from odmantic.bson import ObjectId

from pydantic import BaseModel

#database
class clase(EmbeddedModel):
    asignatura: ObjectId
    puntuacion: float

class Profesor(Model):
    nombres: str
    apellidos: str
    puntuacion: float = 0
    clases: list[clase] = []
    
    model_config = {
        "indexes": lambda: [
            Index(Profesor.apellidos, name="profesor_apellidos")
        ]
    }

class Asignatura(Model):
    nombre: str
    codigo: str
    descripcion: str

    model_config = {
        "indexes": lambda: [
            Index(Asignatura.codigo, name="asignatura_codigo")
        ]
    }

class Comentario(Model):
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    asignatura: ObjectId

    model_config = {
        "indexes": lambda: [
            Index(Comentario.profesor, name="comentario_profesor")
        ]
    }

dbconfig = [Profesor, Asignatura, Comentario]



# RESPONSES
class ProfesorBasic(BaseModel):
    id: ObjectId
    nombres: str
    apellidos: str
    puntuacion: float = 0
    clases: list[clase] = []