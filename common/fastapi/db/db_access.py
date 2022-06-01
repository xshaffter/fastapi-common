import sys

from ..core.parameters import get_param_manager


def get_db_access():
    if 'test' in sys.argv:
        from . import test_db as db_module
    else:
        from . import connection as db_module
    return db_module.get_dal, db_module.get_dal_dependency, db_module.Base, db_module.models, db_module.create_all


get_dal, get_dal_dependency, Base, models, create_all = get_db_access()
