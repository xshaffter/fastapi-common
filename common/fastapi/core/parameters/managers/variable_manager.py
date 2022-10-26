from typing import List

from . import Manager, Environ, Definition


class VariableManager(Manager):
    _backup_data: List = []

    CORS_ORIGINS: List = Environ([])
    DB_DRIVER: str = Environ('postgresql')
    DB_USER: str = Environ(...)
    DB_PASS: str = Environ(...)
    DB_HOST: str = Environ(...)
    DB_PORT: str = Environ(...)
    DB_NAME: str = Environ(...)
    SECRET_KEY: str = Environ(None)
    STATIC_FOLDER: str = Environ(None)
    STATIC_URL: str = Environ(None)

    def backup(self):
        self._backup_data.append(vars(self).copy())

    def restore(self, index=-1):
        if not self._backup_data:
            raise AssertionError('There is no backup to restore')
        backup = self._backup_data.pop(index)
        for key, value in backup.items():
            setattr(self, key, value)
