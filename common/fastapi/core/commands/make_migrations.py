from . import BaseCommand


class MakeMigrationsCommand(BaseCommand):
    help = 'run migrations in case of a declarative base'

    def handle(self, *args, **kwargs):
        from ...db import create_all, Base
        from ..parameters import get_param_manager
        parameters = get_param_manager()
        if parameters.flags.auto_map and not parameters.flags.testing:
            raise ValueError("Your model base must be declarative to make migrations")
        print('Migrating models', ' '.join([model.__name__ for model in Base.__subclasses__()]))
        create_all()
        print('Migrated')
