import re
from typing import TypeVar

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declared_attr

from common.fastapi.core.parameters import get_param_manager


class BaseModel(object):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        snake_class = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return f'{snake_class}s'


parameters = get_param_manager()
vars = parameters.variables

Model = TypeVar("Model", bound=BaseModel)


def query_perform(model: Model, **query):
    query_performed = []
    for key, value in query.items():
        query_performed.append(getattr(model, key) == value)
    print(query_performed)
    return query_performed


def create_connection(driver=vars.DB_DRIVER, user=vars.DB_USER, pwd=vars.DB_PASS, host=vars.DB_HOST, port=vars.DB_PORT,
                      db_name=vars.DB_NAME):
    assert bool(user) == bool(pwd) == bool(host)
    connection_string = ''
    if user and pwd and host:
        connection_string = f"{user}:{pwd}@{host}:{port}"

    connection_string = '/'.join([connection_string, db_name])

    engine = create_engine(
        f"{driver}://{connection_string}",
        pool_size=30,
        max_overflow=40,
        execution_options={
            "isolation_level": "REPEATABLE READ"
        }
    )
    return engine
