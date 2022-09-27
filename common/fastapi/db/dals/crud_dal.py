from typing import TypeVar, Type, List, Generic, get_args

from fastapi import HTTPException

from .base_dal import Dal as BaseDal
from ..utils import query_perform

T = TypeVar("T")


# noinspection PyUnresolvedReferences
class CRUDDal(Generic[T], BaseDal):
    model: Type[T]

    def __init__(self, db, model: Type[T] = None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
        self.model = model or get_args(self.__orig_bases__[0])[0]

    def create(self, data) -> T:
        item = self.model(**data)
        self._db.add(item)

        if self._auto_commit:
            self.commit()
            self._db.refresh(item)
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

    def update(self, data, **query) -> T:
        item_query = self.get_object_query(**query)
        if 'id' in data:
            raise ValueError("updated data cannot include object's id")
        update_data = {getattr(self.model, key): value for key, value in data.items()}
        item_query.update(update_data)

        if self._auto_commit:
            self.commit()
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
