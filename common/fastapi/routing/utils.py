def _action_base(func, method, *args, **kwargs):
    func.request_method = method
    func.args = args
    func.kwargs = kwargs
    return func


def action(method, *args, **kwargs):
    def wrapper(func):
        _action_base(func, method, *args, **kwargs)
        return func
    return wrapper


def get(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'GET', *args, **kwargs)
        return func
    return wrapper


def post(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'POST', *args, **kwargs)
        return func
    return wrapper


def put(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'PUT', *args, **kwargs)
        return func
    return wrapper


def delete(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'DELETE', *args, **kwargs)
        return func
    return wrapper


def head(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'HEAD', *args, **kwargs)
        return func
    return wrapper


def options(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'OPTIONS', *args, **kwargs)
        return func
    return wrapper


def trace(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'TRACE', *args, **kwargs)
        return func
    return wrapper


def patch(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'PATCH', *args, **kwargs)
        return func
    return wrapper


def connect(*args, **kwargs):
    def wrapper(func):
        _action_base(func, 'CONNECT', *args, **kwargs)
        return func
    return wrapper
