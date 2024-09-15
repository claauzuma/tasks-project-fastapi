from typing import Optional
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    completed: bool = False
    deleted: bool = False
    creation: Optional[int] = None
    updated_at: Optional[int] = None

    # Validación que se ejecuta al crear la instancia
    @model_validator(mode='before')
    def set_creation_and_update(cls, values):
        current_timestamp = int(datetime.timestamp(datetime.now()))
        if 'creation' not in values or values['creation'] is None:
            values['creation'] = current_timestamp  # Solo se establece en la creación
        values['updated_at'] = current_timestamp  # Siempre se actualiza al crear o modificar
        return values