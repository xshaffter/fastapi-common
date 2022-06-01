import glob
import json
import os
from typing import List, Union, Dict

from . import BaseCommand
from ..parameters.managers import SysArgv

EXCLUDED_DIRS = [
    '.ds_store', '.idea'
]


def search_model(param: str):
    from ...db import Base
    for model in Base.__subclasses__():
        if model.__name__.lower() == param:
            return model
    return None


def load(filtered: filter):
    from ...db import CRUDDal, get_dal, Base
    for model_data in filtered:
        model: Base = search_model(model_data["model"])
        for data in model_data["data"]:
            dal = get_dal(CRUDDal, model=model)
            result = dal.create(data)


def load_fixtures(models: Union[List, str], base_dir: str = None, dirs: List[str] = None):
    for dir_ in dirs:
        search = os.path.join(base_dir, dir_)
        os.chdir(search)
        for file in glob.glob('*.json'):
            with open(file, 'r') as read_stream:
                data: List[Dict] = json.load(read_stream)
                filtered = filter(lambda group: models == '*' or group["model"] in models, data)
                load(filtered)


class LoadDataCommand(BaseCommand):
    help = 'Load data to fill your DB, you can pass as ' \
           'parameter the models you want to load or dont pass any, to use the entire files'

    models: List = SysArgv('*')

    def handle(self, *args, **kwargs):
        from ..parameters import get_param_manager
        parameters = get_param_manager()
        load_fixtures(self.models, parameters.variables.BASE_DIR, parameters.variables.FIXTURE_DIRS)
