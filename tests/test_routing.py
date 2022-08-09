from fastapi import APIRouter
from fastapi.routing import APIRoute

from common.fastapi.routing import BaseRouter, BaseCRUDRouter
import pytest


@pytest.fixture
def testing_basic_router():
    class TestingBasicRouter(BaseCRUDRouter):
        pass

    return TestingBasicRouter()


@pytest.fixture
def testing_custom_router():
    from common.fastapi.routing import get

    class TestingCustomRouter(BaseCRUDRouter):
        @get('/some_route')
        def some_route(self):
            return {}

    return TestingCustomRouter()


def test_basic_router_functions(testing_basic_router):
    routes = [route.name for route in testing_basic_router.routes]
    assert routes == ['create', 'list', 'update_detail', 'remove', 'detail']


def test_custom_router_functions(testing_custom_router):
    routes = [route.name for route in testing_custom_router.routes]
    assert routes == ['some_route', 'create', 'list', 'update_detail', 'remove', 'detail']


# def test_custom_router_params(testing_custom_router):
#     routes = []
#     for route in testing_custom_router.routes:  # type: APIRoute
#         routes.append(route.)
#     assert routes == ['some_route', 'create', 'list', 'update_detail', 'remove', 'detail']
