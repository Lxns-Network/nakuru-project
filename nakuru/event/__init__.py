from collections import namedtuple
from pydantic import BaseModel

InternalEvent = namedtuple("Event", ("name", "body"))

from .enums import ExternalEventTypes

class ExternalEvent(BaseModel):
    type: ExternalEventTypes