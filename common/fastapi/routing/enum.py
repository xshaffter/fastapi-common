from enum import Enum
from typing import List
from copy import copy
from . import BaseRouter, get
from ..schemas import EnumData


class EnumRouter(BaseRouter):

    def __init__(self, enums=tuple(), *args, **kwargs):
        additional = []
        for cls in Enum.__subclasses__():
            fun_name = cls.__name__.lower()
            if not enums or fun_name in enums:
                action = self.get_action_for_class(copy(cls))
                additional.append(action)
        super(EnumRouter, self).__init__(extra_funcs=additional, *args, **kwargs)

    @staticmethod
    def get_action_for_class(cls):
        fun_name = cls.__name__.lower()
        values = [{'value': t.value, 'display': t.display() if hasattr(t, 'display') else t.name.capitalize()} for t in
                  cls]

        def action():
            return values.copy()

        decorated = get(f"/{fun_name}", response_model=List[EnumData])(action)
        return fun_name, decorated
