import inspect
from types import MethodType
from typing import List


def first_or_none(iterable: filter):
    try:
        value = next(iterable)
    except StopIteration:
        value = None
    return value


def is_view_method(function: MethodType):
    return inspect.ismethod(function) and '__' not in function.__name__ and hasattr(function, 'request_method')


def is_manager_param(field_name, container):
    from ..core.parameters import ManagerParameter
    field_type = type(container.get_field(field_name))
    return issubclass(field_type, ManagerParameter)


def is_bool_param(field, container):
    name, field_type = field
    return is_manager_param(name, container) and field_type is bool


def is_str_param(field, container):
    name, field_type = field
    return is_manager_param(name, container) and field_type is str


def is_list_param(field, container):
    name, field_type = field
    return is_manager_param(name, container) and field_type is List
