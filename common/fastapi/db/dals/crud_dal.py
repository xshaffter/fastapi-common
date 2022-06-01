from typing import TypeVar, Type, List, Generic, get_args

from fastapi import HTTPException

from .base_dal import Dal as BaseDal

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

    def list(self, data=None) -> List[T]:
        items = self._db.query(self.model).all()
        return items

    def get_object_or_404(self, item_id) -> T:
        item = self._db.query(self.model).filter(self.model.id == item_id)
        if not item.first():
            raise HTTPException(404, f'{self.model.__name__} object not found')
        return item

    def detail(self, data) -> T:
        return self.get_object_or_404(data['id']).first()

    def delete(self, **query):
        item = self.detail(**query)
        self._db.delete(item)
        if self._auto_commit:
            self.commit()

    def update(self, data) -> T:
        item = self.get_object_or_404(data['id'])
        update_values = data.copy()
        update_values.pop('id')
        update_data = {getattr(self.model, key): value for key, value in update_values.items()}
        item.update(update_data)

        if self._auto_commit:
            self.commit()
        return item.first()

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
