import typing as T
from enum import Enum
from pydantic import BaseModel

from ..entities import Friend, Member, Anonymous, File, OfflineFile, Device
from ..misc import CQParser

parser = CQParser()

class MessageItemType(Enum):
    FriendMessage = "FriendMessage"
    GroupMessage = "GroupMessage"
    BotMessage = "BotMessage"
    Message = "Message"

class FriendMessage(BaseModel):
    type: MessageItemType = "FriendMessage"
    time: str
    self_id: str
    sub_type: str
    message_id: int
    user_id: int
    message: T.Union[str, list]
    raw_message: str
    font: int
    sender: Friend

    def __init__(self, message: str, **_):
        message = parser.parseChain(message)
        super().__init__(message=message, **_)

class GroupMessage(BaseModel):
    type: MessageItemType = "GroupMessage"
    self_id: int
    sub_type: str
    message_id: int
    group_id: int
    user_id: int
    anonymous: T.Optional[Anonymous]
    message: T.Union[str, list]
    raw_message: str
    font: int
    sender: Member

    def __init__(self, message: str, **_):
        message = parser.parseChain(message)
        super().__init__(message=message, **_)

class BotMessage(BaseModel):
    type: MessageItemType = "BotMessage"
    message_id: int

class Message(BaseModel):  # getMessage
    type: MessageItemType = "Message"
    message_id: int
    real_id: int
    sender: Member
    time: int
    message: str
    raw_message: str

    def __init__(self, message: str, **_):
        message = parser.parseChain(message)
        super().__init__(message=message, **_)

MessageTypes = {
    "private": FriendMessage,
    "group": GroupMessage
}

class ForwardMessageSender(BaseModel):
    nickname: str
    user_id: int

class ForwardMessageNode(BaseModel):
    content: T.Union[str, list]
    raw_content: T.Optional[str] # 本来没有的，用于表示原 content
    sender: ForwardMessageSender
    time: int

    def __init__(self, content: str, **_):
        raw_content = content
        content = parser.parseChain(content)
        super().__init__(content=content, raw_content=raw_content, **_)

class ForwardMessages(BaseModel):
    messages: T.List[ForwardMessageNode]

class NoticeItemType(Enum):
    GroupFileUpload = "GroupFileUpload"
    GroupAdminChange = "GroupAdminChange"
    GroupMemberDecrease = "GroupMemberDecrease"
    GroupMemberIncrease = "GroupMemberIncrease"
    GroupMemberBan = "GroupMemberBan"
    FriendAdd = "FriendAdd"
    GroupMessageRecall = "GroupMessageRecall"
    FriendMessageRecall = "FriendMessageRecall"
    Notify = "Notify"
    GroupCardChange = "GroupCardChange"
    FriendOfflineFile = "FriendOfflineFile"
    ClientStatusChange = "ClientStatusChange"
    EssenceMessageChange = "EssenceMessageChange"

class GroupFileUpload(BaseModel):
    type: NoticeItemType = "GroupFileUpload"
    time: int
    self_id: int
    group_id: int
    user_id: int
    file: File

class GroupAdminChange(BaseModel):
    type: NoticeItemType = "GroupAdminChange"
    time: int
    self_id: int
    sub_type: str
    group_id: int
    user_id: int

class GroupMemberDecrease(BaseModel):
    type: NoticeItemType = "GroupMemberDecrease"
    time: int
    self_id: int
    sub_type: str
    group_id: int
    operator_id: int
    user_id: int

class GroupMemberIncrease(BaseModel):
    type: NoticeItemType = "GroupMemberIncrease"
    time: int
    self_id: int
    sub_type: str
    group_id: int
    operator_id: int
    user_id: int

class GroupMemberBan(BaseModel):
    type: NoticeItemType = "GroupMemberBan"
    time: int
    self_id: int
    sub_type: str
    group_id: int
    operator_id: int
    user_id: int
    duration: int

class FriendAdd(BaseModel):
    type: NoticeItemType = "FriendAdd"
    time: int
    self_id: int
    user_id: int

class GroupMessageRecall(BaseModel):
    type: NoticeItemType = "GroupMessageRecall"
    time: int
    self_id: int
    group_id: int
    user_id: int
    operator_id: int
    message_id: int

class FriendMessageRecall(BaseModel):
    type: NoticeItemType = "FriendMessageRecall"
    time: int
    self_id: int
    user_id: int
    message_id: int

class Notify(BaseModel):
    type: NoticeItemType = "Notify"
    sub_type: str
    user_id: int
    target_id: T.Optional[int]
    time: T.Optional[int]
    self_id: T.Optional[int]
    group_id: T.Optional[int]
    honor_type: T.Optional[str]

class GroupCardChange(BaseModel):
    type: NoticeItemType = "GroupCardChange"
    group_id: int
    user_id: int
    card_new: str
    card_old: str

class FriendOfflineFile(BaseModel):
    type: NoticeItemType = "FriendOfflineFile"
    user_id: int
    file: OfflineFile

class ClientStatusChange(BaseModel):
    type: NoticeItemType = "ClientStatusChange"
    client: Device
    online: bool

class EssenceMessageChange(BaseModel):
    type: NoticeItemType = "EssenceMessageChange"
    sub_type: str
    sender_id: int
    operator_id: int
    message_id: int

NoticeTypes = {
    "group_upload": GroupFileUpload,
    "group_admin": GroupAdminChange,
    "group_decrease": GroupMemberDecrease,
    "group_increase": GroupMemberIncrease,
    "group_ban": GroupMemberBan,
    "friend_add": FriendAdd,
    "group_recall": GroupMessageRecall,
    "friend_recall": FriendMessageRecall,
    "notify": Notify,
    "group_card": GroupCardChange,
    "offline_file": FriendOfflineFile,
    "client_status": ClientStatusChange,
    "essence": EssenceMessageChange
}

class RequestItemType(Enum):
    FriendRequest = "FriendRequest"
    GroupRequest = "GroupRequest"

class FriendRequest(BaseModel):
    type: RequestItemType = "FriendRequest"
    time: int
    self_id: int
    user_id: int
    comment: str
    flag: str

class GroupRequest(BaseModel):
    type: RequestItemType = "GroupRequest"
    time: int
    self_id: int
    sub_type: str
    group_id: int
    user_id: int
    comment: str
    flag: str

RequestTypes = {
    "friend": FriendRequest,
    "group": GroupRequest
}