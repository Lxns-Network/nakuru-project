from .models import *
from enum import Enum

class ExternalEvents(Enum):
    AppInitEvent = AppInitEvent

    GroupFileUpload = GroupFileUpload
    GroupAdminChange = GroupAdminChange
    GroupMemberDecrease = GroupMemberDecrease
    GroupMemberIncrease = GroupMemberIncrease
    GroupMemberBan = GroupMemberBan
    FriendAdd = FriendAdd
    GroupMessageRecall = GroupMessageRecall
    FriendMessageRecall = FriendMessageRecall
    Notify = Notify
    GroupCardChange = GroupCardChange
    FriendOfflineFile = FriendOfflineFile
    ClientStatusChange = ClientStatusChange
    EssenceMessageChange = EssenceMessageChange

    FriendRequest = FriendRequest
    GroupRequest = GroupRequest

class ExternalEventTypes(Enum):
    AppInitEvent = "AppInitEvent"

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

    FriendRequest = "FriendRequest"
    GroupRequest = "GroupRequest"
