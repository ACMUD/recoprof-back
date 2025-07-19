from pydantic import BaseModel, model_validator
from typing import Optional
from odmantic.bson import ObjectId
from typing_extensions import Self

class CommentPostSchema(BaseModel):
    comentario: str
    puntuacion: float = 0
    profesor: ObjectId
    asignatura: ObjectId
    semestre: tuple[int, int]

    @model_validator(mode='after')
    def val_puntuacion(self) -> Self:
        if 0 > self.puntuacion or self.puntuacion >5:
            raise ValueError("Puntuación debe estar entre 0 y 5")
        return self
