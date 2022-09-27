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


operations = [
    'gt',
    'gte',
    'lt',
    'lte',
    'in',
    'contains',
    'iexact',
    'ieq',
    'exact',
    'eq',
]


def define_operation(column: Column, escaped_operation, value):
    eq_result = column == value
    if escaped_operation == 'gt':
        return column > value
    elif escaped_operation == 'gte':
        return column >= value
    elif escaped_operation == 'lt':
        return column < value
    elif escaped_operation == 'lte':
        return column <= value
    elif escaped_operation == 'in':
        return column.in_(value)
    elif escaped_operation == 'contains':
        return column.contains(value)
    elif escaped_operation == 'range':
        cleft, cright = value
        return column.between(cleft, cright)
    elif escaped_operation == 'iexact':
        return value.lower() == column.lower()
    elif escaped_operation == 'ieq':
        return value.lower() == column.lower()
    elif escaped_operation == 'exact':
        return eq_result
    elif escaped_operation == 'eq':
        return eq_result
    elif escaped_operation is None:
        return eq_result
    else:
        raise QueryBuildingException(
            f"{escaped_operation} operation doesn't exist, please use one of the following: {operations}")


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
