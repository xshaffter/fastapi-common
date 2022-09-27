from abc import ABC, abstractmethod
from typing import List, Generic, TypeVar

T = TypeVar("T")


class BaseCommand(ABC):
    command_name = None
    help = 'There is no info for this command'

    @classmethod
    def get_command_name(cls):
        return cls.command_name or cls.__name__.lower().replace('command', '')

    @abstractmethod
    def handle(self, *args, **kwargs):
        pass
