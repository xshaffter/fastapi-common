import os

import pytest

from . import BaseCommand


class PyTestCommand(BaseCommand):
    command_name = 'test'
    help = 'Run tests with db creation'

    def handle(self, *args, **kwargs):
        from ..parameters import get_param_manager
        from ...db import create_all
        parameters = get_param_manager()
        parameters.flags.testing = True
        create_all()
        pytest.main(['-x', '-v'])
