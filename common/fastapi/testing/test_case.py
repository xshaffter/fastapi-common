import os
import re

import pytest
from fastapi.testclient import TestClient

from ..core.app import main_app


class BaseTestCase:
    def __init__(self):
        super(BaseTestCase, self).__init__()
        self.client = TestClient(main_app)

    @classmethod
    def initialize(cls):
        @pytest.fixture(scope="session", autouse=True)
        def cleanup(request):
            """Cleanup a testing directory once we are finished."""

            def remove_test_dir():
                os.remove('test.db')

            request.addfinalizer(remove_test_dir)

        snake_class = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()

        @pytest.fixture(scope='module', name=snake_class)
        def create():
            return cls()
        return cleanup, create
