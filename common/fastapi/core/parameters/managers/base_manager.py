import os
import sys
from abc import ABC
from typing import List, Optional, Callable

from .manager_param import SysArgv, Mixed, Environ, ManagerParameter
from ....utils import first_or_none, is_list_param, is_bool_param, \
    is_str_param


class Manager(ABC):
    _last_index = 2

    def __init__(self, set_params=True):
        if set_params:
            self._set_parameters()

    def __getattr__(self, item):
        try:
            return self.__getattribute__(item)
        except AttributeError:
            return None

    def __str__(self) -> str:
        return f'{type(self).__name__}:{str(self.__dict__)}'

    def get_field(self, field_name):
        return getattr(self, field_name)

    def _get_bool_value(self, field_name) -> bool:
        field: ManagerParameter = self.get_field(field_name)
        field_type = type(field)
        if field_type in [SysArgv, Mixed] and f'--{field_name}' in sys.argv:
            return True
        elif field_type in [Environ, Mixed]:
            return os.environ.get(field_name, False)
        return False

    def _get_str_value(self, field_name) -> Optional[str]:
        field: ManagerParameter = self.get_field(field_name)
        field_type = type(field)
        if field_type in [SysArgv, Mixed]:
            value = first_or_none(filter(lambda param: f'--{field_name}' in param, sys.argv))
            if value:
                return '='.join(value.split('=')[1:])
            elif field_type == SysArgv:
                try:
                    return sys.argv[self._last_index]
                except IndexError:
                    pass
        if field_type in [Environ, Mixed]:
            res = os.environ.get(field_name, None)
            if res is not None:
                return res
        if field_type == Mixed:
            try:
                return sys.argv[self._last_index]
            except IndexError:
                pass

        if field.default is Ellipsis:
            raise ValueError(f'value {field_name} must be setted')
        return field.default

    def _get_list_value(self, field_name) -> Optional[List]:
        field: ManagerParameter = self.get_field(field_name)
        field_type = type(field)
        if field_type in [SysArgv, Mixed] and len(sys.argv) > self._last_index:
            return sys.argv[self._last_index:]
        elif field_type in [Environ, Mixed]:
            param = os.environ.get(field_name, None)
            if param:
                param_as_list = param.split(',')
                return param_as_list

        if field.default is Ellipsis:
            raise ValueError(f'value {field_name} must be setted')
        return field.default

    def _get_field_by_type(self, field_name, field_type):
        if field_type == List:
            return self._get_list_value(field_name)
        elif field_type == str:
            return self._get_str_value(field_name)
        elif field_type == bool:
            return self._get_bool_value(field_name)
        return None

    def _get_parameters_by_predicate(self, predicate: Callable, target=None):
        target_obj = target if target is not None else self
        fields = list(vars(target_obj).items())
        if hasattr(target_obj, '__annotations__'):
            fields += list(target_obj.__annotations__.items())
        return filter(lambda field: predicate(field, self), fields)

    def _set_parameters_by_predicate(self, target, predicate):
        fields = self._get_parameters_by_predicate(predicate)
        errors: List[ValueError] = []
        for field, field_type in fields:
            try:
                value = self._get_field_by_type(field, field_type)
                setattr(target, field, value)
            except ValueError as e:  # type: ValueError
                errors.append(e.args[0])
        if errors:
            raise ValueError(errors)

    def _set_parameters(self):
        self._set_parameters_by_predicate(target=self, predicate=is_bool_param)
        self._set_parameters_by_predicate(target=self, predicate=is_str_param)
        self._set_parameters_by_predicate(target=self, predicate=is_list_param)
