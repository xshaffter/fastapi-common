from typing import Union

from fastapi import APIRouter
from fastapi.routing import APIRoute

from common.fastapi.routing import BaseRouter, BaseCRUDRouter
import pytest


async def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@pytest.fixture
def testing_basic_crud_router():
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


@pytest.fixture
def testing_dependency_router():
    from common.fastapi.routing import get

    class TestingCustomRouter(BaseCRUDRouter):
        def __init__(self, *args, **kwargs):
            from fastapi import Depends
            super(TestingCustomRouter, self).__init__(default_dependencies=[Depends(common_parameters)], *args,
                                                      **kwargs)

        @get('/some_route')
        def some_route(self):
            return {}

    return TestingCustomRouter()


def test_basic_router_functions(testing_basic_crud_router):
    routes = [route.name for route in testing_basic_crud_router.routes]
    assert routes == ['create', 'list', 'update_detail', 'remove', 'detail']


def test_custom_router_functions(testing_custom_router):
    routes = [route.name for route in testing_custom_router.routes]
    assert routes == ['some_route', 'create', 'list', 'update_detail', 'remove', 'detail']


def test_dependency_router_functions(testing_dependency_router):
    for route in testing_dependency_router.routes:  # type: APIRoute
        assert common_parameters in [depend.dependency for depend in route.dependencies]
