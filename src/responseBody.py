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

class ProfesorConAsignatura(ProfesorBase):
    asignaturas_nombre: list[AsignaturasBase] = []

class Token(BaseModel):
    access_token: str
    token_type: str

class AsignaturaTotal(AsignaturasBase):
    facultades: list[FacultadesValidas] = []
# Paginaciones

class BasePaginacion(BaseModel):
    total: int
    total_paginas:int

class PaginacionProfesorBase(BasePaginacion):
    contenido: list[ProfesorBase]

class PaginacionAsignaturasBase(BasePaginacion):
    contenido: list[AsignaturaTotal]

class PaginacionProfesorPorFacultad(BasePaginacion):
    contenido: list[ProfesorPorFacultad]

class PaginacionProfesor(BasePaginacion):
    contenido: list[ProfesorConAsignatura]