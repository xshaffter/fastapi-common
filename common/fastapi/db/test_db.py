import re
from typing import Type

from sqlalchemy import create_engine, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Session, declarative_base, declared_attr
from sqlalchemy import Column

from common.fastapi.core.parameters import get_param_manager
from common.fastapi.db import BaseDal


class BaseModel(object):
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True)

    @declared_attr
    def __tablename__(self):
        cls = type(self)
        snake_class = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return f'{snake_class}s'


parameters = get_param_manager()

engine = create_engine(f"sqlite:///test.db?check_same_thread=False")
async_mode = parameters.flags.ASYNC_MODE

session_class = AsyncSession if async_mode else Session

session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=session_class)

if parameters.flags.auto_map:
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    models = Base.classes
else:
    Base = declarative_base()
    models = None

if async_mode:
    async def get_dal(dal_class: Type[BaseDal], *args, **kwargs):
        async with session() as ses:
            async with ses.begin():
                try:
                    return dal_class(ses, *args, **kwargs)
                finally:
                    ses.close()
else:
    def get_dal(dal_class: Type[BaseDal], *args, **kwargs):
        with session() as ses:
            with ses.begin():
                try:
                    return dal_class(ses, *args, **kwargs)
                finally:
                    ses.close()


def get_dal_dependency(dal_class: Type[BaseDal], *args, **kwargs):
    def wrapper():
        return get_dal(dal_class, *args, **kwargs)

    return wrapper


def create_all():
    Base.metadata.create_all(engine)
