from abc import ABC

from pydantic import BaseModel


class BaseSchema(BaseModel, ABC):
    ...
