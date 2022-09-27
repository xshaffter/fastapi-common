from ...core.parameters import get_param_manager


def get_dal_access():
    params = get_param_manager()
    if params.flags.ASYNC_MODE:
        from .base_dal import AsyncDal as BaseDal
        from .async_crud_dal import AsyncCRUDDal as CRUDDal
    else:
        from .base_dal import Dal as BaseDal
        from .crud_dal import CRUDDal

    return BaseDal, CRUDDal


BaseDal, CRUDDal = get_dal_access()
