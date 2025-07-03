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


LOOKUP_PIPE = []
LOOKUP_PIPE.extend(sort("puntuacion.valor", -1))
LOOKUP_PIPE.extend(lookup("asignatura", "asignaturas", "_id", "asignaturas_info",
                           pipeline = add_fields("id","$_id")))
LOOKUP_PIPE.extend(add_fields("id", "$_id"))
LOOKUP_PIPE.append({"$project": {
        "_id": 0,
        "asignaturas": 0,
    }})

NOTAS = []

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


NOTAS_PROMEDIO = [
 {
        '$unwind': '$puntuaciones'
    }, {
        '$group': {
            '_id': '$puntuaciones.semestre', 
            'valor': {
                '$avg': '$puntuaciones.valor'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'valor': 1, 
            'year': {
                '$arrayElemAt': [
                    '$_id', 0
                ]
            }, 
            'semestre': {
                '$arrayElemAt': [
                    '$_id', 1
                ]
            }
        }
    }, {
        '$sort': {
            'year': 1, 
            'semestre': 1
        }
    }, {
        '$limit': 1
    }, {
        '$project': {
            'valor': 1, 
            'semestre': [
                '$year', '$semestre'
            ]
        }
    }
]