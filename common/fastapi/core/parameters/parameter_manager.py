from .managers import Manager, CommandManager, VariableManager, FlagManager
from ...utils import is_bool_param, is_str_param, is_list_param, Singleton


class ParameterManager(Singleton, Manager):
    def __init__(self):
        self.flags = FlagManager()
        self.commands = CommandManager()
        self.variables = VariableManager()
        self.request_manager = dict()
        super(ParameterManager, self).__init__()

    def _set_parameters(self):
        self._set_parameters_by_predicate(target=self.flags, predicate=is_bool_param)
        self._set_parameters_by_predicate(target=self.variables, predicate=is_str_param)
        self._set_parameters_by_predicate(target=self.variables, predicate=is_list_param)
