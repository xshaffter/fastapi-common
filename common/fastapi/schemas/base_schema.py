from abc import ABC
from enum import Enum
from typing import Dict

from fastapi import Body
from pydantic import BaseModel, root_validator


class BaseSchema(BaseModel, ABC):

    def __init__(self, *args, **kwargs):
        for name, value in dict(self):
            if isinstance(value, Enum):
                display = f"{name}__display"
                setattr(self, display, Body('', description=f"display text for {name} enum value"))

        super().__init__(*args, **kwargs)

    @root_validator
    def get_usage_currency__display(cls, values) -> Dict:
        for name, value in values.items():
            display = f"{name}__display"
            if isinstance(value, Enum) and display in values and values.get(display, None) is None:
                values[display] = value.name.capitalize()
        return values
