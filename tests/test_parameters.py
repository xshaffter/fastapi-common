from common.fastapi.core.parameters import get_param_manager, ParameterManager
from common.fastapi.core.parameters.managers import Mixed, Environ, SysArgv, Definition

import pytest
import os


@pytest.fixture
def param_manager():
    class Params(ParameterManager):
        pass

    return Params


@pytest.fixture
def working_param_manager():
    class Params(ParameterManager):
        var2: str = Environ(...)
        var3: str = Mixed(...)
        var4: str = Definition("value 4")

    return Params


@pytest.fixture
def mixed_manager():
    class Params(ParameterManager):
        var1: str = Definition("value 1")
        var2: bool = SysArgv(...)
        var3: str = Environ("value 4")

    return Params


@pytest.fixture
def not_working_param_manager():
    class Params(ParameterManager):
        var5: str = Definition(...)

    return Params


def test_correct_param_manager(param_manager):
    parameters = get_param_manager()
    assert isinstance(parameters, param_manager)


def test_not_working_param_values_definition(not_working_param_manager):
    try:
        get_param_manager()
        assert False, "var5 should not have a value"
    except ValueError as err:
        assert tuple(*err.args) == ("value var5 must be setted",), "the only error you should get is var5 ValueError"


def test_param_values(working_param_manager):
    os.environ["var2"] = "value 2"
    os.environ["var3"] = "value 3"
    parameters = get_param_manager()

    assert parameters.variables.var2 == "value 2", f"environ var2 should have a value of 'value 2' instead of '{parameters.variables.var2}'"
    assert parameters.variables.var3 == "value 3", f"mixed var3 should have a value of 'value 3' instead of '{parameters.variables.var3}'"
    assert parameters.variables.var4 == "value 4", f"definition var4 should have a value of 'value 4' instead of '{parameters.variables.var4}'"


def test_param_mixed_values(mixed_manager):
    try:
        del os.environ["var2"]
        del os.environ["var3"]
    except KeyError:
        pass

    parameters = get_param_manager()

    assert hasattr(parameters.variables,
                   'var1') and parameters.variables.var1 == "value 1", "var1 should be stored in variables and must have a value of 'value 1'"
    assert hasattr(parameters.flags,
                   'var2') and not parameters.flags.var2, "var2 should be stored in flags and must have a False value"
    assert hasattr(parameters.variables,
                   'var3') and parameters.variables.var3 == "value 4", "var3 should be stored in variables and must have a value of 'value 4'"
