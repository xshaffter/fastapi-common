from typing import Type

class Dal:
    _auto_commit: bool = True

    def __init__(self, db, auto_commit=True, *args, **kwargs):
        self._db = db
        self._auto_commit = auto_commit

    # noinspection PyPep8Naming
    def get_dal(self, DalType: Type['Dal'], *args, **kwargs):
        dal = DalType(db=self._db, auto_commit=False, *args, **kwargs)
        return dal

    def commit(self):
        self._db.commit()

    def flush(self):
        self._db.flush()


class AsyncDal:
    _auto_commit: bool = True

    def __init__(self, db, auto_commit=True, *args, **kwargs):
        self._db = db
        self._auto_commit = auto_commit

    # noinspection PyPep8Naming
    def get_dal(self, DalType: Type['AsyncDal']):
        dal = DalType(db=self._db, auto_commit=False)
        return dal

    async def commit(self):
        await self._db.commit()

    async def flush(self):
        await self._db.flush()
