def get_param_manager():
    from .parameter_manager import ParameterManager

    sub_classes = ParameterManager.__subclasses__()
    if not sub_classes:
        Manager = ParameterManager
    else:
        Manager = sub_classes[-1]
    return Manager.get_instance()
