from abc import ABC
from typing import TypeVar, Generic, get_args

from ..routing import BaseRouter

Model = TypeVar("Model")


class GenericBaseRouter(BaseRouter, ABC, Generic[Model]):
    def __init__(self, *args, **kwargs):
        self.model, = get_args(self.__orig_bases__[0])
        super().__init__(*args, **kwargs)
