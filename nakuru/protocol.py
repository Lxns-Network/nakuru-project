from .entities import *
from .entities.components import Node
from .event.models import BotMessage, Message, ForwardMessages
from .network import fetch


class CQHTTP_Protocol:
    baseurl_http: str

    async def sendFriendMessage(self,
                                user_id: int,
                                group_id: int,
                                message: T.Union[str, list],
                                auto_escape: bool = False) -> T.Union[BotMessage, bool]:
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
                               message: T.Union[str, list],
                               auto_escape: bool = False) -> T.Union[BotMessage, bool]:
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
                                      messages: T.Union[list]) -> T.Union[BotMessage, bool]:
        for i in range(len(messages)):
            if isinstance(messages[i], Node):
                messages[i] = messages[i].toDict()
        result = await fetch.http_post(f"{self.baseurl_http}/send_group_forward_msg", {
            "group_id": group_id,
            "messages": messages
        })
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False

    async def recall(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return True
        return False

    async def getMessage(self, message_id: int) -> T.Union[Message, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return Message.parse_obj(result["data"])
        return False

    async def getForwardMessage(self, message_id: int) -> T.Union[ForwardMessages, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_forward_msg", {
            "message_id": message_id
        })
        if result["status"] == "ok":
            return ForwardMessages.parse_obj(result["data"])
        return False

    async def getImage(self, file: str) -> T.Union[ImageFile, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_image", {
            "file": file
        })
        if result["status"] == "ok":
            return ImageFile.parse_obj(result["data"])
        return False

    async def kick(self,
                   group_id: int,
                   user_id: int,
                   reject_add_request: bool = False) -> bool:
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
                   duration: int = 30 * 60) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_ban", {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration
        })
        if result["status"] == "ok":
            return True
        return False

    async def unmute(self, group_id: int, user_id: int) -> bool:
        return await self.mute(group_id, user_id, 0)

    async def muteAnonymous(self,
                            group_id: int,
                            flag: str,
                            duration: int = 30 * 60,
                            anonymous: Anonymous = None):  # TODO
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
                      enable: bool = True) -> bool:
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
                            enable: bool = True) -> bool:
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
                                enable: bool = True) -> bool:  # TODO go-cqhttp 暂未支持
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
                           card: str = "") -> bool:
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
                           group_name: str) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_name", {
            "group_id": group_id,
            "group_name": group_name
        })
        if result["status"] == "ok":
            return True
        return False

    async def leave(self,
                    group_id: int,
                    is_dismiss: bool = False) -> bool:
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
                                   duration: int = -1) -> bool:
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
                               remark: str = "") -> bool:
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
                              reason: str = "") -> bool:
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

    async def getLoginInfo(self) -> T.Union[Bot, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_login_info")
        if result["status"] == "ok":
            return Bot.parse_obj(result["data"])
        return False

    async def getQiDianAccountInfo(self) -> T.Union[QiDianAccount, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/qidian_get_account_info")
        if result["status"] == "ok":
            return QiDianAccount.parse_obj(result["data"])
        return False

    async def getStrangerInfo(self,
                              user_id: int,
                              no_cache: bool = False) -> T.Union[Stranger, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_stranger_info", {
            "user_id": user_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Stranger.parse_obj(result["data"])
        return False

    async def getFriendList(self) -> T.Union[List[Friend], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_friend_list")
        if result["status"] == "ok":
            return [Friend.parse_obj(friend_info) for friend_info in result["data"]]
        return False

    async def deleteFriend(self,
                           friend_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_friend", {
            "friend_id": friend_id
        })
        if result["status"] == "ok":
            return True
        return False

    async def getUnidirectionalFriendList(self) -> T.Union[List[Friend], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_unidirectional_friend_list")
        if result["status"] == "ok":
            return [Friend.parse_obj(friend_info) for friend_info in result["data"]]
        return False

    async def deleteUnidirectionalFriend(self,
                                         user_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_unidirectional_friend", {
            "user_id": user_id
        })
        if result["status"] == "ok":
            return True
        return False

    async def getGroupInfo(self,
                           group_id: int,
                           no_cache: bool = False) -> T.Union[Group, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Group.parse_obj(result["data"])
        return False

    async def getGroupList(self) -> T.Union[List[Group], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_list")
        if result["status"] == "ok":
            return [Group.parse_obj(group_info) for group_info in result["data"]]
        return False

    async def getGroupMemberInfo(self,
                                 group_id: int,
                                 user_id: int,
                                 no_cache: bool = False) -> T.Union[Member, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_member_info", {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache
        })
        if result["status"] == "ok":
            return Member.parse_obj(result["data"])
        return False

    async def getGroupMemberList(self,
                                 group_id: int) -> T.Union[List[Member], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_member_list", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return [Member.parse_obj(member_info) for member_info in result["data"]]
        return False

    async def getGroupHonorInfo(self,
                                group_id: int,
                                type: str) -> T.Union[Honor, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_honor_info", {
            "group_id": group_id,
            "type": type
        })
        if result["status"] == "ok":
            return Honor.parse_obj(result["data"])
        return False

    async def canSendImage(self) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/can_send_image")
        if result["status"] == "ok":
            if result["data"]["yes"]:
                return True
        return False

    async def canSendRecord(self) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/can_send_record")
        if result["status"] == "ok":
            if result["data"]["yes"]:
                return True
        return False

    async def getVersionInfo(self) -> T.Union[AppVersion, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_version_info")
        if result["status"] == "ok":
            return AppVersion.parse_obj(result["data"])
        return False

    async def restartAPI(self, delay: int = 0) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_restart", {
            "delay": delay
        })
        if result["status"] == "ok":
            return True
        return False

    async def setGroupPortrait(self,
                               group_id: int,
                               file: str,
                               cache: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_restart", {
            "group_id": group_id,
            "file": file,
            "cache": cache
        })
        if result["status"] == "ok":
            return True
        return False

    async def ocrImage(self,
                       image: str) -> T.Union[OCR, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/ocr_image", {
            "image": image
        })
        if result["status"] == "ok":
            return OCR.parse_obj(result["data"])
        return False

    async def getGroupSystemMessage(self) -> T.Union[GroupSystemMessage, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_system_msg")
        if result["status"] == "ok":
            return GroupSystemMessage.parse_obj(result["data"])
        return False

    async def uploadGroupFile(self, group_id: int) -> T.Union[GroupFileSystem, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_file_system_info", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return GroupFileSystem.parse_obj(result["data"])
        return False

    async def getGroupRootFiles(self, group_id: int) -> T.Union[GroupFileTree, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return GroupFileTree.parse_obj(result["data"])
        return False

    async def getGroupFilesByFolder(self,
                                    group_id: int,
                                    folder_id: str) -> T.Union[GroupFileTree, bool]:
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
                              busid: int) -> T.Union[str, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        })
        if result["status"] == "ok":
            return result["data"]["url"]
        return False

    async def getStatus(self) -> T.Union[AppStatus, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_status")
        if result["status"] == "ok":
            return AppStatus.parse_obj(result["data"])
        return False

    async def getGroupAtAllRemain(self, group_id: int) -> T.Union[AtAllRemain, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_at_all_remain", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return AtAllRemain.parse_obj(result["data"])
        return False

    async def getVipInfo(self, user_id: int) -> T.Union[VipInfo, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/_get_vip_info", {
            "user_id": user_id
        })
        if result["status"] == "ok":
            return VipInfo.parse_obj(result["data"])
        return False

    async def sendGroupNotice(self, group_id: int, content: str):
        result = await fetch.http_post(f"{self.baseurl_http}/_send_group_notice", {
            "group_id": group_id,
            "content": content
        })
        if result["status"] == "ok":
            return True
        return False

    async def reloadEventFilter(self, file: str):
        result = await fetch.http_post(f"{self.baseurl_http}/reload_event_filter", {
            "file": file
        })
        if result["status"] == "ok":
            return True
        return False

    async def downloadFile(self, url: str, headers: str, thread_count=1):
        result = await fetch.http_post(f"{self.baseurl_http}/download_file", {
            "url": url,
            "headers": headers,
            "thread_count": thread_count
        })
        if result["status"] == "ok":
            return True
        return False

    async def getOnlineClients(self, no_cashe: bool) -> T.Union[List[Device], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_online_clients", {
            "no_cache": no_cashe
        })
        if result["status"] == "ok":
            return [Device.parse_obj(device) for device in result["data"]["clients"]]
        return False

    async def getGroupMessageHistory(self, group_id: int, message_seq: Optional[int] = None) -> T.Union[List[Message],
                                                                                                        bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_msg_history", {
            "message_seq": message_seq,
            "group_id": group_id
        })
        if result["status"] == "ok":
            print(result)
            return [Message.parse_obj(message) for message in result["data"]["messages"]]
        return False

    async def setEssenceMessage(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_essence_msg", {
            "message_id": message_id
        })  # 草,为什么只有手机看得到
        if result["status"] == "ok":
            return True
        return False

    async def deleteEssenceMessage(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_essence_msg", {
            "message_id": message_id
        })  # 这个我没测试过
        if result["status"] == "ok":
            return True
        return False

    async def getEssenceMessageList(self, group_id: int) -> T.Union[EssenceMessage, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_essence_msg_list", {
            "group_id": group_id
        })
        if result["status"] == "ok":
            return EssenceMessage.parse_obj(result["data"])
        return False

    async def checkURLSafety(self, url: str) -> int:
        result = await fetch.http_post(f"{self.baseurl_http}/check_url_safely", {
            "url": url
        })
        if result["status"] == "ok":
            return result["level"]
        return False

    async def getModelShow(self, model: str) -> T.Union[List[ModelShow], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/_get_model_show", {
            "model": model
        })
        if result["status"] == "ok":
            return [ModelShow.parse_obj(_model) for _model in result["data"]["variants"]]
        return False

    async def setModelShow(self, model: str, model_show: str) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/_set_model_show", {
            "model": model,
            "model_show": model_show
        })
        if result["status"] == "ok":
            return True
        return False
