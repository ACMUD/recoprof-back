from odmantic.bson import ObjectId
from pydantic import BaseModel
from validations.Values import FacultadesValidas

class Puntuacion_prof(BaseModel):
    valor: float = -1
    semestre: tuple[int,int] = (2020,1)

class ProfesorBase(BaseModel):
    id: ObjectId
    nombre: str
    facultades: list[FacultadesValidas]
    puntuacion: Puntuacion_prof = Puntuacion_prof()

class Asignatura(BaseModel):
    id: ObjectId
    nombre: str

class _ComentarioBase(BaseModel):
    id: ObjectId
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    semestre: tuple[int, int]
    up: int = 0
    down: int = 0

class ComentarioBase(_ComentarioBase):
    asignatura: ObjectId

class Comentario(_ComentarioBase):
    asignatura_info: Asignatura

class AsignaturasBase(Asignatura):
    codigo: int

class ProfesorConAsignatura(ProfesorBase):
    asignaturas_info: list[AsignaturasBase] = []

class Token(BaseModel):
    access_token: str
    token_type: str

class AsignaturaTotal(AsignaturasBase):
    facultades: list[FacultadesValidas] = []


class NotasProcesadas(BaseModel):
    puntuaciones: list = []
    asignaturas_info: list[AsignaturasBase] = []
# Paginaciones

class BasePaginacion(BaseModel):
    total: int
    pagina: int
    total_paginas:int

class PaginacionProfesorBase(BasePaginacion):
    contenido: list[ProfesorBase]

class PaginacionAsignaturasBase(BasePaginacion):
    contenido: list[AsignaturaTotal]

class PaginacionProfesor(BasePaginacion):
    contenido: list[ProfesorConAsignatura]

class PaginacionComentario(BasePaginacion):
    contenido: list[Comentario]
