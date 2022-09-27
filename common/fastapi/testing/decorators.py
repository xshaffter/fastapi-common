import functools

from ..core.parameters import get_param_manager


def fake_request_test(*args, **kwargs):
    """
    :param args: unused
    :param kwargs: the custom request you want with the body: [request_manager.service_name][_[function to be faked]]_fakeoption
    e.g.: user_fake_option or user_get_user_by_id_fake_option
    user_fake_option will change every function in your request manager
    user_fake_[function]_option will change just the indicated function
    if you fake a function specifically, and the whole module, the function will have priority
    if you call this without specification, the manager will use the "default" option defined in fake_responses
    :return:
    """
    parameters = get_param_manager()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args2, **kwargs2):
            exception = None
            old_value = parameters.flags.FAKE_REQUESTS
            parameters.flags.FAKE_REQUESTS = True
            try:
                for key, value in kwargs.items():
                    parameters.request_manager[key] = value
                for key, value in kwargs2.items():
                    parameters.request_manager[key] = value
                func(*args2, **kwargs2)
            except AssertionError as err:
                exception = err
            finally:
                for key, value in kwargs.items():
                    del parameters.request_manager[key]
                for key, value in kwargs2.items():
                    del parameters.request_manager[key]
                parameters.flags.FAKE_REQUESTS = old_value

            if exception:
                raise exception

        return wrapper

    return decorator


def fake_parameters(*args, **kwargs):
    parameters = get_param_manager()

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args2, **kwargs2):
            try:
                parameters.variables.backup()
                for key, value in kwargs.items():
                    setattr(parameters.variables, key, value)
                func(*args2, **kwargs2)
            except:
                raise
            finally:
                parameters.variables.restore()

        return wrapper

    return decorator
