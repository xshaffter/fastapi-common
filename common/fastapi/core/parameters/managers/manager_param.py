from enum import Enum, auto
from typing import Generic, TypeVar

T = TypeVar("T")


class ManagerParameter(Generic[T]):
    """
    A generic manager param which receives a type and has a default value
    """
    default: T

    def __init__(self, default: T):
        """

        :rtype: object
        """
        self.default = default


class SysArgv(ManagerParameter[T]):
    """
    A generic manager param which receives a type and has a default value.
    This parameter will be defined by sys.argv parameters only, this way you can ensure that can only be
    overwritten by command line execution
    """


class Environ(ManagerParameter[T]):
    """
    A generic manager param which receives a type and has a default value.
    This parameter will be defined by environment variables only, this way you can ensure that can only be
    overwritten by (as an example) Docker, python-env or os.environ
    """


class Mixed(ManagerParameter[T]):
    """
    A generic manager param which receives a type and has a default value.
    This parameter could be overwritten by sys.argv and os.environ, taking priority from sys.argv, so you can run
    different param, values without needing to overwrite a file
    """


class Definition(ManagerParameter[T]):
    """
    A generic manager param which receives a type and has a default value.
    This is an immutable variable, cannot be overwritten by execution nor environment variables.
    These are for a "project structure dependencies", not for "deployment dependencies"
    """

# TODO: Kubernete
