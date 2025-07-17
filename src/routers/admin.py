from dependencies.repository_access import get_database_engine, get_asignaturas_repository, get_profesor_repository
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from db.models import dbconfig, Asignatura, Profesor
from validations.Values import FacultadesValidas
from typing import Annotated
from dependencies.auth_dep import access
from utils.pdfextract import pdfextract

router = APIRouter(
    tags=["Admin"],
    prefix="/api"
)

@router.post('/configure')
async def configure(acc: Annotated[bool, Depends(access)], engine=Depends(get_database_engine)):
    """
    Utilidad para configurar la base de datos
    """
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    await engine.configure_database(dbconfig, update_existing_indexes=True)
    return {"message": "Database configured successfully"}

@router.post('/materias')
async def materias(
    facultad: FacultadesValidas = Form(), 
    file: UploadFile = File(...), 
    acc: bool = Depends(access), 
    repo_asignaturas = Depends(get_asignaturas_repository), 
    repo_profesores = Depends(get_profesor_repository)
):
    """
    Utilidad para insertar materias a partir de un documento pdf con dichas materias
    PDF;
        cod | materia | Dia | Hora | Edificio | Salon | Profesor
    """
    if not acc:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    materias, profs = await pdfextract(file.file)

    ids = {}

    for materia in materias:
        mat_db = await repo_asignaturas.get_asignatura_by_code(materia[0])
        if not mat_db:
            mat_db = Asignatura(codigo=materia[0], nombre=materia[1])

        mat_db.facultades = list(set(mat_db.facultades + [facultad]))

        mat_db = await repo_asignaturas.create_asignatura(mat_db)
        ids[materia[0]] = mat_db.id

    for p in profs:
        prof_db = await repo_profesores.get_profesor_list(name=p, limit=1)
        if len(prof_db) > 0:
            prof_db = prof_db[0] if isinstance(prof_db, list) else prof_db
            prof_db = Profesor(**prof_db)
        else:
            prof_db = None
        if prof_db is None:
            prof_db = Profesor(nombre=p)

        prof_db.asignaturas = list(set(prof_db.asignaturas + [ids[i] for i in profs[p]]))
        prof_db.facultades = list(set(prof_db.facultades + [facultad]))
        await repo_profesores.create_profesor(prof_db)
    
    return {"materias": materias, "profesores": list(profs.keys()), "message": "Data imported successfully"}
