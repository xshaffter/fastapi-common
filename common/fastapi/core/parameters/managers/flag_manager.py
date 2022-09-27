from . import Manager
from .manager_param import Mixed


class FlagManager(Manager):
    ASYNC_MODE: bool = Mixed(False)
    auto_map: bool = Mixed(False)
    DEBUG: bool = Mixed(False)
    FAKE_REQUESTS: bool = Mixed(False)
