from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from ..parameters import get_param_manager

app = FastAPI()
parameter = get_param_manager()

origins = parameter.variables.CORS_ORIGINS
if origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"]
    )
if parameter.variables.STATIC_URL:
    app.mount(parameter.variables.STATIC_URL, StaticFiles(directory=parameter.variables.STATIC_FOLDER), 'static')


def execute():
    parameter.commands.perform_command()
