from abc import ABC


class Singleton(ABC):
    instance: object = None

    def __init__(self):
        super(Singleton, self).__init__()
        cls = type(self)
        if cls.instance and isinstance(cls.instance, cls):
            raise ReferenceError('Singleton cannot be re instantiated')

    @classmethod
    def get_instance(cls):
        if not cls.instance or not isinstance(cls.instance, cls):
            cls.instance = cls()
        return cls.instance
