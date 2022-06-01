import abc
import sys
import types
from abc import ABC
from typing import Callable, Tuple, Union, Dict

import requests
from fastapi.exceptions import HTTPException

from . import ResponseType
from ..core.parameters import get_param_manager

response_types = Union[str, Dict, bytes]


class RequestManagerException(HTTPException):
    pass


class BaseRequestManager(ABC):
    fake_response = {
        'default': {
            'response': {
                "accumulated_size": 15,
            },
            "status_code": 200
        }
    }

    # noinspection PyUnresolvedReferences,PyProtectedMember
    @staticmethod
    def _get_fun_name(n=0):
        return sys._getframe(n + 1).f_code.co_name

    @property
    @abc.abstractmethod
    def service_url(self):
        """
        which url will this service go e.g.: https://localhost:8000/
        :return:
        """
        pass

    @property
    @abc.abstractmethod
    def service_name(self):
        """
        which name will your service be called as in the fake_response functionality
        :return:
        """
        pass

    @classmethod
    def _get_fake_response(cls):
        parameters = get_param_manager()
        faked_request_name = cls._get_fun_name(2)
        fun_option = f"{cls.service_name}_{faked_request_name}_fake_option"
        cls_option = f"{cls.service_name}_fake_option"
        fake_fun_option = parameters.request_manager.get(fun_option)
        fake_cls_option = parameters.request_manager.get(cls_option, 'default')
        fake_option = fake_fun_option or fake_cls_option
        response = cls.fake_response[fake_option]
        json_response = response["response"]
        status_code = response["status_code"]
        return status_code, json_response

    @classmethod
    def _do_request(cls, method: Callable, endpoint: str, response_type: ResponseType = ResponseType.json,
                    raise_exception=True, *args, **kwargs) -> Tuple[int, response_types]:
        parameters = get_param_manager()
        if parameters.flags.testing and parameters.flags.FAKE_REQUESTS:
            status_code, response = cls._get_fake_response()
        else:
            request = method(f'{cls.service_url}/{endpoint}', *args, **kwargs)
            status_code = request.status_code
            response = getattr(request, response_type.name)
            if isinstance(response, types.FunctionType) or isinstance(response, types.MethodType):
                response = response()

        if raise_exception and status_code >= 400:
            raise RequestManagerException(status_code=status_code, detail=response)
        return status_code, response

    @classmethod
    def get(cls, *args, **kwargs):
        return cls._do_request(requests.get, *args, **kwargs)

    @classmethod
    def post(cls, *args, **kwargs):
        return cls._do_request(requests.post, *args, **kwargs)

    @classmethod
    def put(cls, *args, **kwargs):
        return cls._do_request(requests.put, *args, **kwargs)

    @classmethod
    def patch(cls, *args, **kwargs):
        return cls._do_request(requests.patch, *args, **kwargs)

    @classmethod
    def head(cls, *args, **kwargs):
        return cls._do_request(requests.head, *args, **kwargs)

    @classmethod
    def options(cls, *args, **kwargs):
        return cls._do_request(requests.options, *args, **kwargs)

    @classmethod
    def delete(cls, *args, **kwargs):
        return cls._do_request(requests.delete, *args, **kwargs)
