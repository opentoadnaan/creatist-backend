from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI

from src.utils import UserHandler  # type: ignore  # noqa

load_dotenv()
user_handler = UserHandler()

HOST = os.environ["HOST"]
PORT = os.environ["PORT"]


async def startup():
    await user_handler.init()


app = FastAPI(title="Creatist API Documentation", on_startup=[startup])

from .routes import *  # noqa
