# fastapi-common

This library helps with pre-made modules, configurations and classes to make easier the fastapi applications
development.

## Installation
```shell
pip install fastapi-common
```

## installation dependencies @ 0.2.0
 - optional requirements marked by \*dependency\*

| Library          | Version |
|------------------|---------|
| ***FastApi***    | 0.73.0  |
| ***SQLAlchemy*** | 1.4.31  |
| ***Requests***   | 2.27.1  |
| ***Pydantic***   | 1.9.0   |
| ***Uvicorn***    | 0.17.5  |
| ***PyTest***     | 7.0.1   |

## Usage

Every module has its own usage, which you will find bellow separated according to the module

### DB

this module is initialized automatically by ParameterManager info with environment variables:

```python
DB_DRIVER: str = 'postgresql'  # has default value as postgresql DB
DB_USER: str
DB_PASS: str
DB_HOST: str
DB_NAME: str
ASYNC_MODE: bool = False  # will determine if database session is asynchronous or not
auto_map: bool = False  # True: load models from DB, False: load DB from models 
```

also, has submodules, which help with a certain functionality:

#### get_dal

this function helps you with getting a DAL by a centralized way

```python
from common.fastapi.db import get_dal_dependency


@post('/example/url')
def example(session: FileDAL = Depends(get_dal_dependency(FileDAL, ...))):
    pass


@post('/example/url')
def example(session: FileDAL = Depends(get_dal_dependency(CRUDDal[File], ...))):
    pass


@post('/example/url')
def example(session: FileDAL = Depends(get_dal_dependency(CRUDDal, File, ...))):
    pass
```

#### Base

this is the Base so you can create your models, if you are in auto_map mode, remember to add this property to the model
so you can use it without conflicts

```python
__table_args__ = {'extend_existing': True}
```

#### models

this property, is only available if you use auto_map mode, this way you can access to your models

```python
from common.fastapi.db import models

session.query(models.User).filter(User.id == 1).first()
```

#### create_all

this function just creates the database with all the tables, more like an initialization

```python
from common.fastapi.db import create_all

create_all()
```

### ParameterManager

This whole module receives info that is needed for the execution, has default values to be received, but you can add
more.

```python
# import this way to be able to override info and add new values
from common.fastapi import ParameterManager
from common.fastapi.core.parameters.managers import SysArgv, Environ, Definition, Mixed


class MyParameters(
    ParameterManager):  # Extend the ParameterManager class so the common will know how to interpret everything

    STATIC_URL: str = SysArgv(
        "/static_files")  # with this, the string could be passed as a param like "--static_url=/static" otherwise, will take a default value of "/static_files"

    EXCLUDE: bool = SysArgv(
        False)  # this boolean should be passed by console app call as "--exclude" param and if not passed, the default value would be False

    STATIC_URL: str = Environ(
        "/static_files")  # with this definition, the value for STATIC_URL will be only defined by environment variables, and won't be affected by console params

    AUTO_MAP: bool = Environ(
        False)  # same as above, but the value of this variable will be stored in instance.flags.AUTO_MAP

    STATIC_URL: str = Definition(
        "/static_files")  # This won't be affected by anything, but it's recommended to use to be putted on it's right place

    STATIC_URL: str = Mixed(
        "/static_files")  # This one will be affected by SysArgv and Environ, in that priority, so it will be a fully mutable variable

    STATIC_URL: str = Environ(
        ...)  # With this, the variable won't have a default value, use this only in variables that should not be stored in plain code

    IS_PRODUCTION: bool = Environ(
        ...)  # you should not use booleans with Ellipsis, because if there is no flag, then the value should be False


# in any other file
# if you want to access to your ParameterManager and don't have import errors use this way
from common.fastapi import get_param_manager

parameters = get_param_manager()
do_something(parameters.variables.STATIC_URL)
```

### BaseCommand

This thing is a command manager which eases the creation of tasks that should run from your console

```shell
python main.py runserver
```

as an example, we will recreate this command

```python
import uvicorn

from common.fastapi.core.commands import BaseCommand
from common.fastapi.core.parameters.managers import SysArgv


class RunServerCommand(BaseCommand):
    help = 'run server application with uvicorn package'  # this is unused by the moment, but should work as a --help flag for every command (might be changed to __docs__)

    host: str = SysArgv('0.0.0.0:8000')

    def handle(self, *args, **kwargs):
        host, port = self.host.split(':')
        uvicorn.run("enroute.common.fastapi.core.app:main_app", host=host, port=int(port), reload=True)

```

### Available commands and its params:

- runserver --host=0.0.0.0:8000
- loaddata model1 model2 model3
- makemigrations (creates tables, might use real migrations in a future)
- test (runs testing and prepares testing db)

### testing

#### decorators

***fake_request_test*** decorator will help you to fake raquests between micro services (you may see more info in it's
documentation)

#### BaseTestCase

Use this to access to the TestClient and initialize test database, inheriting from it and calling this way:

```python
from common.fastapi.db import get_dal, CRUDDal
from common.fastapi.testing import fake_request_test, BaseTestCase
from db.models import Video


class VideoTestData(BaseTestCase):

    def __init__(self):
        super(VideoTestData, self).__init__()
        dal = get_dal(CRUDDal, Video)
        self.video: Video = dal.create({
            "user_id": 10,
            "byte_size": 1024,
            "url": "http://localhost:8000/",
            "path": "/app/static/some_filename",
            "file_name": "some_filename",
            "extension": "txt"
        })

    def get_root_token(self):
        return 'let\'s supose this is a coherent token'


cleanup, video_test = VideoTestData.initialize()
```

### requests

#### ResponseType

```python
from common.fastapi.requests import ResponseType

ResponseType.json  # returns the result of RequestManager as json call it as
ResponseType.content  # returns the result of RequestManager as content bytes call it as
ResponseType.text  # returns the result of RequestManager as text call it as
```

#### RequestManager

This class manages requests from another services with a centralized functionality, this way you can manage everything
without making all by yourself.

```python
from common.fastapi.requests import BaseRequestManager

from common.fastapi import get_param_manager
from common.fastapi.requests import ResponseType


class MembershipRequestManager(BaseRequestManager):
    fake_response = {
        'default': {  # Every option needs a "response" and a "status_code" to work, don't forget it
            'response': {
                "name": "Basic",
                "max_disk_space": 1024
            },
            "status_code": 200
        }
    }
    service_url = get_param_manager().variables.MEMBERSHIPS_URL  # this is the url that will be used to reffer the service 
    service_name = 'membership'  # this is for fake_response management only

    @classmethod
    def get_membership_by_id(cls, membership_id):
        status, json_response = cls.get(f'membership/detail/{membership_id}',
                                        ResponseType.json)  # This way you can tell the manager that you want a json response (default is json, so you may not put it) 
        return json_response
```

### Routing

#### utilss

#### BaseRouter

this class manages every http method decorated function in the class, so it can make them urls

#### CRUDRouters

this class makes the same as **BaseRouter**, but includes CRUD routes for a model passed as a field of the class

```python
from common.fastapi.routing import post, BaseCRUDRouter, get

from db.models import Video


class VideoRouter(BaseCRUDRouter):
    model = Video
```

#### GenericRouters

this two classes are a mirror of BaseRouter and BaseCRUDRouter, but with the particularity that they use Generic types (as seen below)

```python
from common.fastapi.routing import post, GenericBaseCRUDRouter, get

from db.models import Video


class VideoRouter(GenericBaseCRUDRouter[Video]):
    pass
```