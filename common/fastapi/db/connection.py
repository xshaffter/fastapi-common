from typing import Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from . import BaseDal
from .utils import create_connection, BaseModel
from ..core.parameters import get_param_manager

parameters = get_param_manager()
async_mode = parameters.flags.ASYNC_MODE
vars = parameters.variables

engine = create_connection(driver=vars.DB_DRIVER.split(':')[0])

session_class = AsyncSession if async_mode else Session

if parameters.flags.auto_map:
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    models = Base.classes
else:
    Base = declarative_base(cls=BaseModel)
    models = None
if async_mode:
    engine = create_connection()

T = TypeVar("T", bound=BaseDal)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=session_class, expire_on_commit=False)

if async_mode:
    async def get_dal(dal_class: Type[T], *args, **kwargs) -> T:
        async with session() as ses:
            async with ses.begin():
                try:
                    return dal_class(ses, *args, **kwargs)
                finally:
                    await ses.close()
else:
    def get_dal(dal_class: Type[T], *args, **kwargs) -> T:
        with session() as ses:
            with ses.begin():
                try:
                    return dal_class(ses, *args, **kwargs)
                finally:
                    ses.close()


def get_dal_dependency(dal_class: Type[T], *args, **kwargs):
    def wrapper():
        return get_dal(dal_class, *args, **kwargs)

    return wrapper


def create_all():
    Base.metadata.create_all(engine)
