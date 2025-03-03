from db.engine import Engine
from db.models import dbconfig, Asignatura, Profesor
from validations.Values import FacultadesValidas
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from typing import Annotated
from .auth import access

from utils.pdfextract import pdfextract

router = APIRouter(
    tags=["Admin"],
    prefix="/api"
)

@router.post('/configure')
async def configure(acc: Annotated[bool, Depends(access)]):
    """
    Utilidad para configurar la base de datos
    """
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await Engine.configure_database(dbconfig,update_existing_indexes=True)

@router.post('/materias')
async def materias(facultad:FacultadesValidas = Form(), YY: int = Form(), periodo: int = Form(), file: UploadFile = File(...), acc: bool = Depends(access)):
    """
    Utilidad para insertar materias a partir de un documento pdf con dichas materias
    PDF;
        cod | materia | Dia | Hora | Edificio | Salon | Profesor
    """
    materias, profs = await pdfextract(file.file)
    for materia in materias:
        mat_db = await Engine.find_one(Asignatura, Asignatura.codigo == materia[0])
        if mat_db is None:
            await Engine.save(Asignatura(codigo=materia[0], nombre=materia[1]))
    for p in profs:
        prof_db = await Engine.find_one(Profesor, Profesor.nombre == p)
        if prof_db is None:
            profesor = Profesor(nombre=p, facultad=facultad, clases=profs[p])
            await Engine.save(profesor)
        else:
            tmpclases = prof_db.clases+tmpclases
            tmpclases = list(set(tmpclases))
            await Engine.save(prof_db, clases=tmpclases)
    return materias