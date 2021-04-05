from pydantic import BaseModel

class Member(BaseModel):
    user_id: int
    nickname: str
    card: str
    sex: str
    age: int
    area: str
    level: str
    role: str
    title: str

class Anonymous(BaseModel):
    id: int
    name: str
    flag: str