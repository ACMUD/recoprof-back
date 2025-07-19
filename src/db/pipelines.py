import re

def paginacion(
    page: int = 0,
    limit: int = 10
):
    return [
        { "$skip": page * limit },
        { "$limit": limit }
    ]

def match(
    field: str,
    value: str,
    regex: bool = True
):
    return [{
        "$match": {
            field: ({ "$regex": re.compile(f".*{re.escape(value)}.*", re.IGNORECASE) } if regex else value)
        }
    }]

def lookup(
    from_collection: str,
    local_field: str,
    foreign_field: str,
    as_: str,
    pipeline: list = None
):
    return [{
        "$lookup": {
            "from": from_collection,
            "localField": local_field,
            "foreignField": foreign_field,
            "as": as_,
            "pipeline": pipeline
        }
    }]

def add_fields(
    field: str,
    value: str
):
    return [{
        "$addFields": {
            field: value
        }
    }]

def unset(
    field: str
):
    return [{
        "$unset": field
    }]

def unwind(
    field: str
):
    return [{
        "$unwind": field
    }]

def sort(
    field: str,
    order: int = 1
):
    return [{
        "$sort": {
            field: order
        }
    }]


LOOKUP_PIPE: list[dict] = []
LOOKUP_PIPE.extend(sort("puntuacion.valor", -1))
LOOKUP_PIPE.extend(lookup("asignatura", "asignaturas", "_id", "asignaturas_info",
                           pipeline = add_fields("id","$_id")))
LOOKUP_PIPE.extend(add_fields("id", "$_id"))
LOOKUP_PIPE.append({"$project": {
        "_id": 0,
        "asignaturas": 0,
    }})

NOTAS: list[dict] = []

NOTAS.extend(lookup("asignatura", "asignatura", "_id", "asignaturas_info",
                        [{"$addFields": {"id": "$_id"}},
                        {"$project": {
                            "_id":0
                        }}]
                        ))
NOTAS.extend(unset("_id"))
NOTAS.extend(unset("profesor"))
NOTAS.extend(unset("asignatura"))
NOTAS.extend(add_fields("id", "$_id"))


NOTAS_PROMEDIO:list[dict] = []
NOTAS_PROMEDIO. extend(unwind("$puntuaciones"))
NOTAS_PROMEDIO. extend([
    {
        '$group': {
            '_id': '$puntuaciones.semestre',
            'promedio': {
                '$avg': '$puntuaciones.valor'
            }
        }
    }, {
        '$sort': {
            '_id.0': 1,
            '_id.1': 1
        }
    }
])

PROMEDIO_GLOBAL: list[dict] = []
PROMEDIO_GLOBAL.extend(unwind("$puntuaciones"))
PROMEDIO_GLOBAL.extend([{
        '$group': {
            '_id': '$profesor',
            'promedio': {
                '$avg': '$puntuaciones.valor'
            }
        }
    }])
PROMEDIO_GLOBAL.extend(unset("_id"))
