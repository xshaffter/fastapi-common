import re
from typing import TypeVar

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import declared_attr

from common.fastapi.core.parameters import get_param_manager


class QueryBuildingException(Exception):
    pass


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


def get_refs(key: str):
    try:
        column, escape = key.split('__')
    except:
        column = key
        escape = None

    return column, escape


def define_operation(column: Column, escaped_operation, value):
    eq_result = column == value
    results = {
        'gt': column > value,
        'gte': column >= value,
        'lt': column < value,
        'lte': column <= value,
        'in': column.in_(value),
        'contains': column.contains(value),
        'iexact': value.lower() == column.lower(),
        'ieq': value.lower() == column.lower(),
        'exact': eq_result,
        'eq': eq_result
    }
    if escaped_operation in results:
        return results[escaped_operation]
    elif escaped_operation is None:
        return eq_result
    else:
        raise QueryBuildingException(
            f"{escaped_operation} operation doesn't exist, please use one of the following: {results.keys()}")


def query_perform(model: Model, **query):
    query_performed = []
    for key, value in query.items():
        column, escape = get_refs(key)
        column_ref = getattr(model, column)
        defined_operation = define_operation(column_ref, escape, value)
        query_performed.append(defined_operation)
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
