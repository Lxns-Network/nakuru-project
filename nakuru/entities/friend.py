from pydantic import BaseModel

class Friend(BaseModel):
    user_id: int
    nickname: str
    sex: str
    age: int