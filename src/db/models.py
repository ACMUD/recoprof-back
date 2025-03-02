from odmantic import Model, Index, EmbeddedModel
from odmantic.bson import ObjectId
from validations.Values import FacultadesValidas

#database
class Puntuacion(EmbeddedModel):
    valor: float
    cantidad: int
    semestre: tuple[int,int]

class Notas(Model):
    asignatura: str
    profesor: ObjectId
    puntuaciones: list[Puntuacion] = []

    model_config = {
        "indexes": lambda: [
            Index(Notas.profesor, name="notas profesor"),
            Index(Notas.asignatura, name="notas asignatura"),
            Index(Notas.asignatura, Notas.profesor, name="notas asignatura profesor")
        ]
    }

class Profesor(Model):
    nombres: str
    apellidos: str
    facultad: FacultadesValidas
    puntuacion: float = 0
    Cantidad: int = 0
    clases: list[str] = []
    
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
    semestre: tuple[int,int]
    model_config = {
        "indexes": lambda: [
            Index(Comentario.profesor, name="comentario profesor"),
            Index(Comentario.semestre, name="comentario semestre")
        ]
    }

dbconfig = [Profesor, Asignatura, Comentario, Notas]