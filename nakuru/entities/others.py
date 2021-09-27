from pydantic import BaseModel, Field
from typing import Optional

class Bot(BaseModel):
    user_id: int
    nickname: str

class QiDianAccount(BaseModel):
    master_id: int
    ext_name: str
    create_time: int

class Stranger(BaseModel):
    user_id: int
    nickname: str
    sex: str
    age: int
    qid: str

class AppVersion(BaseModel):
    app_name: str
    app_version: str
    app_full_name: str
    protocol_version: str
    coolq_edition: str
    coolq_directory: str
    go_cqhttp: bool = Field(..., alias="go-cqhttp")
    plugin_version: str
    plugin_build_number: int
    plugin_build_configuration: str
    runtime_version: str
    runtime_os: str
    version: str
    protocol: int

class NetworkStatistics(BaseModel):
    packet_received: int
    packet_sent: int
    packet_lost: int
    message_received: int
    message_sent: int
    disconnect_times: int
    lost_times: int

class AppStatus(BaseModel):
    app_initialized: bool
    app_enabled: bool
    plugins_good: bool
    app_good: bool
    online: bool
    good: bool
    stat: NetworkStatistics

class TextDetection(BaseModel):
    text: str
    confidence: int
    coordinates: str

class OCR(BaseModel):
    texts: TextDetection
    language: str

class InvitedRequest(BaseModel):
    request_id: int
    invitor_uin: int
    invitor_nick: str
    group_id: int
    group_name: str
    checked: bool
    actor: int

class JoinRequest(BaseModel):
    request_id: int
    requester_uin: int
    requester_nick: str
    message: str
    group_id: int
    group_name: str
    checked: bool
    actor: int

class GroupSystemMessage(BaseModel):
    invited_requests: Optional[InvitedRequest]
    join_requests: Optional[JoinRequest]

class VipInfo(BaseModel):
    user_id: int
    nickname: str
    level: int
    level_speed: float
    vip_level: str
    vip_growth_speed: int
    vip_growth_total: int

class EssenceMessage(BaseModel):
    sender_id: int
    sender_nick: int
    sender_time: int
    operator_id: int
    operator_nick: int
    operator_time: int
    message_id: int

class ModelInfo(BaseModel):
    model_show: str
    need_pay: bool

class ModelShou(BaseModel):
    variants: List[ModelInfo]
