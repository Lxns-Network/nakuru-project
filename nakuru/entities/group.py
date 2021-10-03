from pydantic import BaseModel
from typing import Optional
import typing as T

class Member(BaseModel):
    user_id: int
    nickname: str
    card: T.Optional[str]
    sex: str
    age: int
    area: str
    level: str
    role: T.Optional[str]
    title: T.Optional[str]
    # 以下是 getGroupMemberInfo 返回的更多结果
    group_id: Optional[int]
    join_time: Optional[int]
    last_sent_time: Optional[int]
    unfriendly: Optional[bool]
    title_expire_time: Optional[int]
    card_changeable: Optional[bool]
    shut_up_timestamp: Optional[int]

class Anonymous(BaseModel):
    id: int
    name: str
    flag: str

class Group(BaseModel):
    group_id: int
    group_name: str
    group_memo: str
    group_create_time: int
    group_level: int
    member_count: int
    max_member_count: int

class HonorListNode(BaseModel):
    user_id: int
    nickname: str
    avatar: str
    description: Optional[str]
    day_count: Optional[int]

class Honor(BaseModel):
    group_id: int
    current_talkative: Optional[HonorListNode]
    talkative_list: Optional[T.List[HonorListNode]]
    performer_list: Optional[T.List[HonorListNode]]
    legend_list: Optional[T.List[HonorListNode]]
    strong_newbie_list: Optional[T.List[HonorListNode]]
    emotion_list: Optional[T.List[HonorListNode]]

class AtAllRemain(BaseModel):
    can_at_all: bool
    remain_at_all_count_for_group: int
    remain_at_all_count_for_uin: int