from enum import Enum

from .models import *


class ExternalEvents(Enum):
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
