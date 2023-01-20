from typing import TypeVar, Type, List, Generic, get_args, Union, Dict

from fastapi import HTTPException
from sqlalchemy.orm import RelationshipProperty
from pydantic import BaseModel
from sqlalchemy import func

from .base_dal import Dal as BaseDal
from ..utils import query_perform

T = TypeVar("T")


# noinspection PyUnresolvedReferences
class CRUDDal(Generic[T], BaseDal):
    model: Type[T]

    def __init__(self, db, model: Type[T] = None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
        self.model = model or get_args(self.__orig_bases__[0])[0]

    def create(self, data: Union[BaseModel, Dict]):
        if isinstance(data, BaseModel):
            return self._create(data)
        elif isinstance(data, Dict):
            return self.__create(data)

    def _get_last_id(self):
        result = self._db.query(func.max(self.model.id)).first()
        return result[0] or 0

    def _create(self, data: BaseModel) -> T:
        variables = dict(data)
        clean_data = dict(data)
        nested = filter(lambda item: isinstance(item[1], BaseModel), variables.items())
        for key, value in nested:
            clean_data.pop(key)
            sub_dal = self.get_dal(CRUDDal, model=value.Config.model)
            instance = sub_dal.create(value)
            clean_data[f"{key}_id"] = instance.id
        return self.__create(clean_data)

    def __create(self, data: Dict) -> T:
        item = self.model(**data)
        self._db.add(item)
        last_id = self._get_last_id()
        item.id = last_id + 1

        if self._auto_commit:
            self.commit()
            self._db.refresh(item)
        else:
            self.flush()
        return item

    def list(self, **query) -> List[T]:
        query_performed = query_perform(self.model, **query)
        items = self._db.query(self.model).filter(*query_performed).all()
        return items

    def get_object_or_404(self, **query) -> T:
        item = self.get_object(**query)
        if not item:
            raise HTTPException(404, f'{self.model.__name__} object not found')
        return item

    def get_object(self, **query):
        query_performed = query_perform(self.model, **query)

        result = self._db.query(self.model).filter(*query_performed)
        return result.first()

    def get_object_query(self, **query):
        query_performed = query_perform(self.model, **query)

        result = self._db.query(self.model).filter(*query_performed)
        return result

    def detail(self, **query) -> T:
        return self.get_object_or_404(**query)

    def delete(self, **query):
        item = self.detail(**query)
        self._db.delete(item)
        if self._auto_commit:
            self.commit()

    def update(self, data: BaseModel, **query) -> T:
        item_query = self.get_object_query(**query)
        if 'id' in data:
            raise ValueError("updated data cannot include object's id")
        update_data = {getattr(self.model, key): value for key, value in data.items()}
        item_query.update(update_data)

        if self._auto_commit:
            self.commit()
        else:
            self.flush()
        return item_query.first()

    @classmethod
    def bulk_create(cls, data, bulk_count):
        dal: cls = get_dal(cls, auto_commit=False)
        for count, item in enumerate(data):
            dal.create(item)
            if count != 0 and count % bulk_count == 0:
                print(f"bulked {count} rows")
                dal.commit()
                dal: cls = get_dal(cls, auto_commit=False)
        dal.commit()
