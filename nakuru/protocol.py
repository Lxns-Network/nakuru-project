import typing as T

from .event.models import BotMessage, Message, Anonymous
from .entities.file import ImageFile
from .network import fetch

class CQHTTP_Protocol:
    baseurl_http: str

    async def sendFriendMessage(self,
                                friend_id: int,
                                group_id: str,
                                group: int = 0,
                                auto_escape: bool = False
                                ):
        result = await fetch.http_post(f"{self.baseurl_http}/send_private_msg", {
            "friend_id": friend_id,
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False
        

    async def sendGroupMessage(self,
                               group_id: int,
                               message: str,
                               auto_escape: bool = False
                               ):
        result = await fetch.http_post(f"{self.baseurl_http}/send_group_msg", {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False
    
    async def sendGroupForwardMessage(self, group_id: int, messages):
        pass  # TODO sendGroupForwardMessage

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
        pass  # TODO getForwardMessage
    
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