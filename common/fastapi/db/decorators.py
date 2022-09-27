import functools


def atomic():
    from common.fastapi.db import BaseDal

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            origin: BaseDal = args[0]
            if not isinstance(origin, BaseDal):
                raise ValueError("Decorated function must belong to BaseDal sub classes")
            origin._auto_commit = False
            try:
                func(*args, **kwargs)
                origin.commit()
            except:
                origin._db.rollback()

        return wrapper

    return decorator
