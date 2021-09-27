import typing as T

from pydantic import BaseModel


class Friend(BaseModel):
    user_id: int
    nickname: str
    sex: T.Optional[str]
    age: T.Optional[int]
    source: T.Optional[str]
