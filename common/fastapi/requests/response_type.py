from enum import Enum, auto


class ResponseType(Enum):
    json = auto()
    content = auto()
    text = auto()
