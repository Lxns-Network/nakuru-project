from pydantic import BaseModel
import typing as T

class Depend:
    def __init__(self, func, middlewares=[], cache=True):
        self.func = func
        self.middlewares = middlewares
        self.cache = cache

class ExecutorProtocol(BaseModel):
    callable: T.Callable
    dependencies: T.List[Depend]
    middlewares: T.List

    class Config:
        arbitrary_types_allowed = True

from . import InternalEvent
from pydantic import BaseModel

class UnexpectedException(BaseModel):
    error: Exception
    event: InternalEvent

    class Config:
        arbitrary_types_allowed = True