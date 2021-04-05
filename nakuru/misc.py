import asyncio
import inspect
import os
import random
import re
import traceback
import typing as T
from collections import namedtuple
from enum import Enum
from threading import Lock, Thread

import aiohttp

from .logger import Protocol, Session


Parameter = namedtuple("Parameter", ["name", "annotation", "default"])

TRACEBACKED = os.urandom(32)

def raiser(error):
    raise error

def protocol_log(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            Protocol.info(f"protocol method {func.__name__} was called")
            return result
        except Exception as e:
            Protocol.error(f"protocol method {func.__name__} raised a error: {e.__class__.__name__}")
            raise e

    return wrapper

def argument_signature(callable_target) -> T.List[Parameter]:
    return [
        Parameter(
            name=name,
            annotation=param.annotation if param.annotation != inspect._empty else None,
            default=param.default if param.default != inspect._empty else None
        )
        for name, param in dict(inspect.signature(callable_target).parameters).items()
    ]