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
async def materias(facultad:FacultadesValidas = Form(), file: UploadFile = File(...), acc: bool = Depends(access)):
    """
    Utilidad para insertar materias a partir de un documento pdf con dichas materias
    PDF;
        cod | materia | Dia | Hora | Edificio | Salon | Profesor
    """
    materias, profs = await pdfextract(file.file)

    ids = {}

    for materia in materias:
        mat_db = await Engine.find_one(Asignatura, Asignatura.codigo == materia[0])
        if not mat_db:
            mat_db = Asignatura(codigo=materia[0], nombre=materia[1])
        
        mat_db.facultades = list(set(mat_db.facultades + [facultad]))
        
        mat_db = await Engine.save(mat_db)
        ids[materia[0]]=mat_db.id

    for p in profs:
        prof_db = await Engine.find_one(Profesor, Profesor.nombre == p)
        if prof_db is None:
            prof_db = Profesor(nombre=p)

        prof_db.asignaturas = list(set(prof_db.asignaturas+[ids[i] for i in profs[p]]))
        prof_db.facultades = list(set(prof_db.facultades + [facultad]))
        await Engine.save(prof_db)
    return materias