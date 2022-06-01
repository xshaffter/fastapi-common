from typing import TypeVar, Type, List, Generic, get_args

from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.future import select

from .base_dal import AsyncDal

T = TypeVar("T")


# noinspection PyUnresolvedReferences
class AsyncCRUDDal(Generic[T], AsyncDal):
    model: Type[T]

    def __init__(self, db, model: Type[T] = None, *args, **kwargs):
        super().__init__(db, *args, **kwargs)
        self.model = model or get_args(self.__orig_bases__[0])[0]

    async def create(self, data) -> T:
        item = self.model(**data)
        self._db.add(item)

        if self._auto_commit:
            await self.commit()
            await self._db.refresh(item)
        return item

    async def list(self, data=None) -> List[T]:
        stmt = select(self.model)
        result = await self._db.execute(stmt)
        return result.scalars()

    def get_object_or_404(self, **query) -> T:
        item = self.get_object(**query)
        if not item:
            raise HTTPException(404, f'{self.model.__name__} object not found')
        return item

    async def get_object(self, **query):
        query_performed = True
        for key, value in query.items():
            query_performed = query_performed and getattr(self.model, key) == value

        stmt = select(self.model).filter(query_performed)
        result = await self._db.execute(stmt)
        return result.scalars().first()

    def detail(self, **query) -> T:
        return self.get_object_or_404(**query)

    async def delete_all(self):
        query = delete(self.model)
        await self._db.execute(query)
        await self._db.commit()

    async def delete(self, **query):
        item = self.detail(**query)
        self._db.delete(item)
        if self._auto_commit:
            await self.commit()

    async def update(self, data) -> T:
        item = self.get_object_or_404(id=data['id'])
        update_values = data.copy()
        update_values.pop('id')
        update_data = {getattr(self.model, key): value for key, value in update_values.items()}
        item.update(update_data)

        if self._auto_commit:
            await self.commit()
        return item.first()

    @classmethod
    async def bulk_create(cls, data, bulk_count):
        from . import get_dal
        dal: cls = await get_dal(cls, auto_commit=False)
        for count, item in enumerate(data):
            await dal.create(item)
            if count != 0 and count % bulk_count == 0:
                print(f"bulked {count} rows")
                await dal.commit()
                dal: cls = await get_dal(cls, auto_commit=False)
        await dal.commit()