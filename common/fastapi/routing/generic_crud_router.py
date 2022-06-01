from abc import ABC
from typing import TypeVar, Generic, get_args

from ..routing import BaseCRUDRouter
from pydantic import BaseModel as BaseSchema

Model = TypeVar("Model")
Schema = TypeVar("Schema", bound=BaseSchema)
RequestSchema = TypeVar("RequestSchema", bound=BaseSchema)


class GenericBaseCRUDRouter(BaseCRUDRouter, ABC, Generic[Model, Schema, RequestSchema]):
    def __init__(self, *args, **kwargs):
        self.model, self.schema, self.request_schema = get_args(self.__orig_bases__[0])
        super().__init__(*args, **kwargs)
