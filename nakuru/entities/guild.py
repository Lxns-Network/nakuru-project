from pydantic import BaseModel
from typing import Optional, List
import typing as T

class BotGuild(BaseModel):
    nickname: str
    tiny_id: int
    avatar_url: str

class Guild(BaseModel):
    guild_id: int
    guild_name: str
    guild_display_id: Optional[int]
    # 以下是 getGuildMetaByGuest 返回的更多结果
    guild_profile: Optional[str]
    create_time: Optional[int]
    max_member_count: Optional[int]
    max_robot_count: Optional[int]
    max_admin_count: Optional[int]
    member_count: Optional[int]
    owner_id: Optional[int]

class SlowMode(BaseModel):
    slow_mode_key: int
    slow_mode_text: str
    speak_frequency: int
    slow_mode_circle: int

class Channel(BaseModel):
    owner_guild_id: int
    channel_id: int
    channel_type: int
    channel_name: str
    create_time: int
    creator_id: int
    creator_tiny_id: int
    talk_permission: int
    visible_type: int
    current_slow_mode: int
    slow_modes: List[SlowMode]

class GuildMember(BaseModel):
    tiny_id: Optional[int]
    user_id: Optional[int]
    title: Optional[str]
    nickname: str
    role: Optional[int]

class GuildMembers(BaseModel):
    members: List[GuildMember]
    bots: List[GuildMember]
    admins: List[GuildMember]

class Reaction(BaseModel):
    emoji_id: str
    emoji_index: int
    emoji_type: int
    emoji_name: str
    count: int
    clicked: bool