import typing as T

from .event.models import BotMessage, Message, Anonymous, ForwardMessages
from .entities import *
from .network import fetch

class CQHTTP_Protocol:
    baseurl_http: str

    async def sendFriendMessage(self,
                                user_id: int,
                                group_id: int,
                                message,
                                auto_escape: bool = False) -> BotMessage:
        if isinstance(message, list):
            _message = ""
            for chain in message:
                _message += chain.toString()
            message = _message
        result = await fetch.http_post(f"{self.baseurl_http}/send_private_msg", {
            "user_id": user_id,
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False
        

    async def sendGroupMessage(self,
                               group_id: int,
                               message,
                               auto_escape: bool = False) -> BotMessage:
        if isinstance(message, list):
            _message = ""
            for chain in message:
                _message += chain.toString()
            message = _message
        result = await fetch.http_post(f"{self.baseurl_http}/send_group_msg", {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False
    
    async def sendGroupForwardMessage(self,
                                      group_id: int,
                                      messages: list):
        # TODO 构造 messages，现在也可以直接用该链接的格式发送：https://docs.go-cqhttp.org/cqcode/#%E5%90%88%E5%B9%B6%E8%BD%AC%E5%8F%91%E6%B6%88%E6%81%AF%E8%8A%82%E7%82%B9
        result = await fetch.http_post(f"{self.baseurl_http}/send_group_forward_msg", {
            "group_id": group_id,
            "messages": messages
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False

    async def recall(self, message_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/delete_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return True
        return False

    async def getMessage(self, message_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return Message.parse_obj(result["data"])
        return False
    
    async def getForwardMessage(self, message_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_forward_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return ForwardMessages.parse_obj(result["data"])
        return False
    
    async def getImage(self, file: str):
        result = await fetch.http_post(f"{self.baseurl_http}/get_image", {
            "file": file
        })
        if result["status"] == "ok":
            return ImageFile.parse_obj(result["data"])
        return False
    
    async def kick(self,
                   group_id: int,
                   user_id: int,
                   reject_add_request: bool = False):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_kick", {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def mute(self,
                   group_id: int,
                   user_id: int,
                   duration: int = 30 * 60):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_ban", {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def unmute(self, group_id: int, user_id: int):
        return await self.mute(group_id, user_id, 0)

    async def muteAnonymous(self,
                            group_id: int,
                            flag: str,
                            duration: int = 30 * 60,
                            anonymous: Anonymous = None):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_anonymous_ban", {
            "group_id": group_id,
            "flag": flag,
            "duration": duration
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def muteAll(self,
                      group_id: int,
                      enable: bool = True):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_whole_ban", {
            "group_id": group_id,
            "enable": enable
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupAdmin(self,
                            group_id: int,
                            user_id: int,
                            enable: bool = True):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_admin", {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupAnonymous(self,
                                group_id: int,
                                user_id: int,
                                enable: bool = True):  # TODO go-cqhttp 暂未支持
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupCard(self,
                           group_id: int,
                           user_id: int,
                           card: str = ""):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_card", {
            "group_id": group_id,
            "user_id": user_id,
            "card": card
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupName(self,
                           group_id: int,
                           group_name: str):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_name", {
            "group_id": group_id,
            "group_name": group_name
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def leave(self,
                    group_id: int,
                    is_dismiss: bool = False):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_leave", {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupSpecialTitle(self,
                                   group_id: int,
                                   user_id: int,
                                   special_title: str = "",
                                   duration: int = -1):
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_special_title", {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setFriendRequest(self,
                               flag: str,
                               approve: bool = True,
                               remark: str = ""):
        result = await fetch.http_post(f"{self.baseurl_http}/set_friend_add_request", {
            "flag": flag,
            "approve": approve,
            "remark": remark
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupRequest(self,
                              flag: str,
                              sub_type: str,
                              approve: bool = True,
                              reason: str = ""):
        if sub_type not in ["add", "invite"]:
            return False
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_add_request", {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
            "reason": reason
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def getLoginInfo(self):
        result = await fetch.http_post(f"{self.baseurl_http}/get_login_info")
        if result["status"] == "ok":
            return Bot.parse_obj(result["data"])
        return False
    
    async def getQiDianAccountInfo(self):
        result = await fetch.http_post(f"{self.baseurl_http}/qidian_get_account_info")
        if result["status"] == "ok":
            return QiDianAccount.parse_obj(result["data"])
        return False
    
    async def getStrangerInfo(self,
                              user_id: int,
                              no_cache: bool = False):
        result = await fetch.http_post(f"{self.baseurl_http}/get_stranger_info", {
            "user_id": user_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Stranger.parse_obj(result["data"])
        return False
    
    async def getFriendList(self):
        result = await fetch.http_post(f"{self.baseurl_http}/get_friend_list")
        if result["status"] == "ok":
            return [Friend.parse_obj(friend_info) for friend_info in result["data"]]
        return False
    
    async def deleteFriend(self,
                         friend_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/delete_friend", {
            "friend_id": friend_id
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def getGroupInfo(self,
                           group_id: int,
                           no_cache: bool = False):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Group.parse_obj(result["data"])
        return False
        
    async def getGroupList(self):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_list")
        if result["status"] == "ok":
            return [Group.parse_obj(group_info) for group_info in result["data"]]
        return False
    
    async def getGroupMemberInfo(self,
                                 group_id: int,
                                 user_id: int,
                                 no_cache: bool = False):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_member_info", {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Member.parse_obj(result["data"])
        return False
    
    async def getGroupMemberList(self,
                                 group_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_member_list", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return [Member.parse_obj(member_info) for member_info in result["data"]]
        return False
    
    async def getGroupHonorInfo(self,
                                group_id: int,
                                type: str) -> Honor:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_honor_info", {
            "group_id": group_id,
            "type": type
        })
        if result["status"] == "ok":
            return Honor.parse_obj(result["data"])
        return False
    
    async def canSendImage(self):
        result = await fetch.http_post(f"{self.baseurl_http}/can_send_image")
        if result["status"] == "ok":
            if result["data"]["yes"]:
                return True
        return False
    
    async def canSendRecord(self):
        result = await fetch.http_post(f"{self.baseurl_http}/can_send_record")
        if result["status"] == "ok":
            if result["data"]["yes"]:
                return True
        return False
    
    async def getVersionInfo(self) -> AppVersion:
        result = await fetch.http_post(f"{self.baseurl_http}/get_version_info")
        if result["status"] == "ok":
            return AppVersion.parse_obj(result["data"])
        return False
    
    async def restartAPI(self,
                         delay: int = 0):
        result = await fetch.http_post(f"{self.baseurl_http}/set_restart", {
            "delay": delay
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def setGroupPortrait(self,
                               group_id: int,
                               file: str,
                               cache: int):
        result = await fetch.http_post(f"{self.baseurl_http}/set_restart", {
            "group_id": group_id,
            "file": file,
            "cache": cache
        })
        if result["status"] == "ok":
            return True
        return False
    
    async def ocrImage(self,
                       image: str) -> OCR:
        result = await fetch.http_post(f"{self.baseurl_http}/ocr_image", {
            "image": image
        })
        if result["status"] == "ok":
            return OCR.parse_obj(result["data"])
        return False
    
    async def getGroupSystemMessage(self):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_system_msg")
        if result["status"] == "ok":
            return GroupSystemMessage.parse_obj(result["data"])
        return False
    
    async def uploadGroupFile(self,
                              group_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_file_system_info", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return GroupFileSystem.parse_obj(result["data"])
        return False
    
    async def getGroupRootFiles(self,
                                group_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return GroupFileTree.parse_obj(result["data"])
        return False
    
    async def getGroupFilesByFolder(self,
                                    group_id: int,
                                    folder_id: str):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id,
            "folder_id": folder_id
        })
        if result["status"] == "ok":
            return GroupFileTree.parse_obj(result["data"])
        return False
    
    async def getGroupFileURL(self,
                              group_id: int,
                              file_id: str,
                              busid: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        })
        if result["status"] == "ok":
            return result["data"]["url"]
        return False
    
    async def uploadGroupFile(self):
        result = await fetch.http_post(f"{self.baseurl_http}/get_status")
        if result["status"] == "ok":
            return AppStatus.parse_obj(result["data"])
        return False
    
    async def getGroupAtAllRemain(self,
                                  group_id: int):
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_at_all_remain", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return AtAllRemain.parse_obj(result["data"])
        return False
    
    async def getVipInfo(self):
        # TODO 获取 VIP 信息
        pass
    
    async def sendGroupNotice(self):
        # TODO 发送群公告
        pass
    
    async def reloadEventFilter(self):
        # TODO 重载事件过滤器
        pass
    
    async def downloadFile(self):
        # TODO 下载文件到缓存目录
        pass
    
    async def getOnlineClients(self):
        # TODO 获取当前账号在线客户端列表
        pass
    
    async def getGroupMessageHistory(self):
        # TODO 获取群消息历史记录
        pass
    
    async def setEssenceMessage(self):
        # TODO 设置精华消息
        pass
    
    async def deleteEssenceMessage(self):
        # TODO 移出精华消息
        pass
    
    async def getEssenceMessageList(self):
        # TODO 获取精华消息列表
        pass
    
    async def checkURLSafety(self):
        # TODO 检查链接安全性
        pass
    
    async def getModelShow(self):
        # TODO 获取在线机型
        pass
    
    async def setModelShow(self):
        # TODO 设置在线机型
        pass