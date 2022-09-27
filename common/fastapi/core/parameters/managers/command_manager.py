import sys
from typing import List, Type, Dict, TypeVar, Callable

from . import Manager
from ...commands import BaseCommand
from ....utils import first_or_none, is_bool_param, is_str_param, is_list_param

Command = TypeVar("Command", bound=BaseCommand)


class CommandManager(Manager):
    available_commands: Dict[str, Command] = dict()
    used_command_obj: Command = None
    _last_index = 2

    @staticmethod
    def find_commands():
        values: List[Type[Command]] = BaseCommand.__subclasses__()
        return {value.get_command_name(): value() for value in values}

    def __init__(self):
        super(CommandManager, self).__init__(set_params=False)
        self.load_commands()

    def get_field(self, field_name):
        return getattr(self.used_command_obj, field_name, None)

    def _set_parameters_by_predicate(self, target, predicate):
        fields = self._get_parameters_by_predicate(predicate, target=target)
        for field, field_type in fields:
            value = self._get_field_by_type(field, field_type)
            setattr(target, field, value)

    def _set_parameters(self):
        self._set_parameters_by_predicate(target=self.used_command_obj, predicate=is_str_param)
        self._set_parameters_by_predicate(target=self.used_command_obj, predicate=is_bool_param)
        self._set_parameters_by_predicate(target=self.used_command_obj, predicate=is_list_param)

    def perform_command(self):
        self.load_values()
        if not self.used_command_obj:
            return
        self._set_parameters()
        self.used_command_obj.handle()

    def load_commands(self):
        available_commands = self.find_commands()
        self.available_commands = available_commands

    def load_values(self):
        param = first_or_none(filter(lambda param_f: param_f in self.available_commands.keys(), sys.argv))
        self._last_index = sys.argv.index(param) + 1
        self.used_command_obj = self.available_commands.get(param)
