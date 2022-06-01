import inspect
from abc import ABC
from typing import Type, List, Tuple, Union

from fastapi import APIRouter

from ..utils.functions import is_view_method


# noinspection PyUnresolvedReferences,PyTypeChecker
class BaseRouter(APIRouter, ABC):
    """
    This Class based router, will manage your views to be fastapi friendly
    just use the enroute.common.fastapi.routing.[http method] decorators
    """
    model: Type = None

    def __init__(self, extra_funcs: Union[Tuple[Tuple], List[Tuple]] = tuple(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        methods = inspect.getmembers(self, predicate=is_view_method)
        meth_names = [name for name, func in methods]
        filtered_extra = [(name, func) for name, func in extra_funcs if name not in meth_names]
        actions = methods + filtered_extra
        for name, action in actions:
            action_func = None
            action.kwargs['name'] = name
            if hasattr(self, 'schema'):
                if 'response_model' not in action.kwargs:
                    action.kwargs['response_model'] = self.schema
                elif action.kwargs['response_model'] is List:
                    action.kwargs['response_model'] = List[self.schema]

            if 'summary' not in action.kwargs:
                action.kwargs['summary'] = getattr(action, '__docs__', None)
            if action.request_method == 'GET':
                action_func = self.get(*action.args, **action.kwargs)
            elif action.request_method == 'POST':
                action_func = self.post(*action.args, **action.kwargs)
            elif action.request_method == 'PUT':
                action_func = self.put(*action.args, **action.kwargs)
            elif action.request_method == 'DELETE':
                action_func = self.delete(*action.args, **action.kwargs)
            elif action.request_method == 'HEAD':
                action_func = self.head(*action.args, **action.kwargs)
            elif action.request_method == 'OPTIONS':
                action_func = self.options(*action.args, **action.kwargs)
            elif action.request_method == 'TRACE':
                action_func = self.trace(*action.args, **action.kwargs)
            elif action.request_method == 'PATCH':
                action_func = self.patch(*action.args, **action.kwargs)
            elif action.request_method == 'CONNECT':
                action_func = self.connect(*action.args, **action.kwargs)

            if action_func:
                action_func(action)
