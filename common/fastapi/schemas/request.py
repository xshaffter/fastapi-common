from typing import Generic, TypeVar, Union

from fastapi import Body
from pydantic.generics import GenericModel

from . import BaseSchema

TypeX = TypeVar("TypeX", bound=BaseSchema)


class BasicRequestSchema(GenericModel, Generic[TypeX]):
    data: TypeX = Body(None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class RemovedSchema(BaseSchema):
    removed: bool


class EnumData(BaseSchema):
    value: Union[int, str]
    display: str
