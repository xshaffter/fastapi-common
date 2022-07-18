import uvicorn

from . import BaseCommand
from ..parameters.managers import SysArgv


class RunServerCommand(BaseCommand):
    help = 'run server application with uvicorn package'

    host: str = SysArgv('0.0.0.0:8000')

    def handle(self, *args, **kwargs):
        host, port = self.host.split(':')
        uvicorn.run("common.fastapi.core.app:main_app", host=host, port=int(port), reload=True)
