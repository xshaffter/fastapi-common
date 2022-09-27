from typing import Type


class Dal:
    _auto_commit: bool = True

    def __init__(self, db, auto_commit=True, *args, **kwargs):
        self._db = db
        self._auto_commit = auto_commit

    # noinspection PyPep8Naming
    def get_dal(self, DalType: Type['Dal']):
        dal = DalType(self._db, False)
        return dal

    def commit(self):
        self._db.commit()


class AsyncDal:
    _auto_commit: bool = True

    def __init__(self, db, auto_commit=True, *args, **kwargs):
        self._db = db
        self._auto_commit = auto_commit

    # noinspection PyPep8Naming
    def get_dal(self, DalType: Type['AsyncDal']):
        dal = DalType(self._db, False)
        return dal

    async def commit(self):
        await self._db.commit()
