from abc import ABC
from typing import Type, List

from fastapi import Depends
from pydantic import BaseModel as BaseSchema

from . import get, post, put, delete, BaseRouter
from ..db import CRUDDal, get_dal_dependency
from ..schemas import BasicRequestSchema, HTTPResponseModel, HTTP_200_REMOVED, HTTP_200_UPDATED, \
    HTTP_201_CREATED


class BaseCRUDRouter(BaseRouter, ABC):
    model: Type = None
    schema: Type[BaseSchema] = None
    request_schema: Type[BaseSchema] = None

    def __init__(self, *args, **kwargs):
        funcs = self.create_views()
        super().__init__(funcs, *args, **kwargs)

    def create_views(self):
        request_schema = BasicRequestSchema[self.request_schema]

        @get('/', response_model=List)
        async def list(dal: CRUDDal = Depends(get_dal_dependency(CRUDDal, model=self.model))):
            items = dal.list()
            return items

        @get('/detail/{id}')
        async def detail(id: int, dal: CRUDDal = Depends(get_dal_dependency(CRUDDal, model=self.model))):
            item = dal.detail(id=id)
            return item

        @delete('/detail/{id}', response_model=HTTPResponseModel)
        async def remove(id: int, dal: CRUDDal = Depends(get_dal_dependency(CRUDDal, model=self.model))):
            dal.delete(id=id)
            return HTTP_200_REMOVED

        @put('/detail/{id}', response_model=HTTPResponseModel)
        async def update_detail(id: int, request: request_schema,
                                dal: CRUDDal = Depends(get_dal_dependency(CRUDDal, model=self.model))):
            data = request.data
            dal.update(data, id=id)
            return HTTP_200_UPDATED

        @post('/create', response_model=HTTPResponseModel)
        async def create(request: request_schema,
                         dal: CRUDDal = Depends(get_dal_dependency(CRUDDal, model=self.model))):
            data = request.data
            dal.create(data)
            return HTTP_201_CREATED

        return ('create', create), ('list', list), ('update_detail', update_detail), ('remove', remove), (
            'detail', detail)
