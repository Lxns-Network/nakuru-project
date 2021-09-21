from pydantic import BaseModel
import typing as T

class Friend(BaseModel):
    user_id: int
    nickname: str
    sex: T.Optional[str]
    age: T.Optional[int]
    source: T.Optional[str]