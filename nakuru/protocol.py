import typing as T

from .event.models import BotMessage, Message, Anonymous, ForwardMessages
from .entities import *
from .entities.components import Node
from .network import fetch


class CQHTTP_Protocol:
    baseurl_http: str
    protocol_params: dict = {}

    async def sendFriendMessage(self,
                                user_id: int,
                                message: T.Union[str, list],
                                group_id: T.Optional[int] = None,
                                auto_escape: bool = False) -> T.Union[BotMessage, bool]:
        if isinstance(message, list):
            _message = ""
            for chain in message:
                _message += chain.toString()
            message = _message
        payload = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape
        }
        if group_id:
            payload["group_id"] = group_id
        result = await fetch.http_post(f"{self.baseurl_http}/send_private_msg", payload, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False

    async def sendGroupForwardMessage(self,
                                      group_id: int,
                                      messages: list) -> T.Union[BotMessage, bool]:
        for i in range(len(messages)):
            if isinstance(messages[i], Node):
                messages[i] = messages[i].toDict()
        result = await fetch.http_post(f"{self.baseurl_http}/send_group_forward_msg", {
            "group_id": group_id,
            "messages": messages
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False
    
    async def sendPrivateForwardMessage(self,
                                        user_id: int,
                                        messages: list) -> T.Union[BotMessage, bool]:
        for i in range(len(messages)):
            if isinstance(messages[i], Node):
                messages[i] = messages[i].toDict()

        result = await fetch.http_post(f"{self.baseurl_http}/send_private_forward_msg", {
            "user_id": user_id,
            "messages": messages
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False

    async def recall(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_msg", {
            "message_id": message_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getMessage(self, message_id: int) -> T.Union[Message, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_msg", {
            "message_id": message_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return Message.parse_obj(result["data"])
        return False

    async def getForwardMessage(self, message_id: int) -> T.Union[ForwardMessages, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_forward_msg", {
            "message_id": message_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return ForwardMessages.parse_obj(result["data"])
        return False

    async def getImage(self, file: str) -> T.Union[ImageFile, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_image", {
            "file": file
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def muteAll(self,
                      group_id: int,
                      enable: bool = True) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_whole_ban", {
            "group_id": group_id,
            "enable": enable
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def setGroupAnonymous(self,
                                group_id: int,
                                enable: bool = True) -> bool:  # TODO go-cqhttp 暂未支持
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_anonymous", {
            "group_id": group_id,
            "enable": enable
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def setGroupName(self,
                           group_id: int,
                           group_name: str) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_name", {
            "group_id": group_id,
            "group_name": group_name
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def leave(self,
                    group_id: int,
                    is_dismiss: bool = False) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_group_leave", {
            "group_id": group_id,
            "is_dismiss": is_dismiss
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getLoginInfo(self) -> T.Union[Bot, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_login_info", params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getGroupInfo(self,
                           group_id: int,
                           no_cache: bool = False) -> T.Union[Group, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_info", {
            "group_id": group_id,
            "no_cache": no_cache
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return Member.parse_obj(result["data"])
        return False

    async def getGroupMemberList(self,
                                 group_id: int) -> T.Union[List[Member], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_member_list", {
            "group_id": group_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [Member.parse_obj(member_info) for member_info in result["data"]]
        return False

    async def getGroupHonorInfo(self,
                                group_id: int,
                                type: str) -> T.Union[Honor, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_honor_info", {
            "group_id": group_id,
            "type": type
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def ocrImage(self,
                       image: str) -> T.Union[OCR, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/ocr_image", {
            "image": image
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return GroupFileSystem.parse_obj(result["data"])
        return False

    async def getGroupRootFiles(self, group_id: int) -> T.Union[GroupFileTree, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return GroupFileTree.parse_obj(result["data"])
        return False

    async def getGroupFilesByFolder(self,
                                    group_id: int,
                                    folder_id: str) -> T.Union[GroupFileTree, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_root_files", {
            "group_id": group_id,
            "folder_id": folder_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return GroupFileTree.parse_obj(result["data"])
        return False

    async def getGroupFileURL(self,
                              group_id: int,
                              file_id: str,
                              busid: int) -> T.Union[str, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_file_url", {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid
        }, params=self.protocol_params)
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
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return AtAllRemain.parse_obj(result["data"])
        return False

    async def getVipInfo(self, user_id: int) -> T.Union[VipInfo, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/_get_vip_info", {
            "user_id": user_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return VipInfo.parse_obj(result["data"])
        return False

    async def sendGroupNotice(self, group_id: int, content: str):
        result = await fetch.http_post(f"{self.baseurl_http}/_send_group_notice", {
            "group_id": group_id,
            "content": content
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def reloadEventFilter(self, file: str):
        result = await fetch.http_post(f"{self.baseurl_http}/reload_event_filter", {
            "file": file
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def downloadFile(self, url: str, headers: str, thread_count=1):
        result = await fetch.http_post(f"{self.baseurl_http}/download_file", {
            "url": url,
            "headers": headers,
            "thread_count": thread_count
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getOnlineClients(self, no_cashe: bool) -> T.Union[List[Device], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_online_clients", {
            "no_cache": no_cashe
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [Device.parse_obj(device) for device in result["data"]["clients"]]
        return False

    async def getGroupMessageHistory(self, group_id: int, message_seq: Optional[int] = None) -> T.Union[List[Message], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_group_msg_history", {
            "message_seq": message_seq,
            "group_id": group_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            print(result)
            return [Message.parse_obj(message) for message in result["data"]["messages"]]
        return False

    async def setEssenceMessage(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/set_essence_msg", {
            "message_id": message_id
        }, params=self.protocol_params)  # 草,为什么只有手机看得到
        if result["status"] == "ok":
            return True
        return False

    async def deleteEssenceMessage(self, message_id: int) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/delete_essence_msg", {
            "message_id": message_id
        }, params=self.protocol_params)  # 这个我没测试过
        if result["status"] == "ok":
            return True
        return False

    async def getEssenceMessageList(self, group_id: int) -> T.Union[EssenceMessage, bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/get_essence_msg_list", {
            "group_id": group_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return EssenceMessage.parse_obj(result["data"])
        return False

    async def checkURLSafety(self, url: str) -> int:
        result = await fetch.http_post(f"{self.baseurl_http}/check_url_safely", {
            "url": url
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return result["level"]
        return False

    async def getModelShow(self, model: str) -> T.Union[List[ModelShow], bool]:
        result = await fetch.http_post(f"{self.baseurl_http}/_get_model_show", {
            "model": model
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [ModelShow.parse_obj(_model) for _model in result["data"]["variants"]]
        return False

    async def setModelShow(self, model: str, model_show: str) -> bool:
        result = await fetch.http_post(f"{self.baseurl_http}/_set_model_show", {
            "model": model,
            "model_show": model_show
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getGuildServiceProfile(self) -> T.Union[BotGuild, bool]:
        '''
        获取频道系统内BOT的资料
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_service_profile")
        if result["status"] == "ok":
            return BotGuild.parse_obj(result["data"])
        return False

    async def getGuildList(self) -> T.Union[list, bool]:
        '''
        获取频道列表
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_list")
        if result["status"] == "ok":
            return [Guild.parse_obj(_guild) for _guild in result["data"]]
        return False

    async def getGuildMetaByGuest(self, guild_id: int) -> T.Union[Guild, bool]:
        '''
        通过访客获取频道元数据
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_meta_by_guest", {
            "guild_id": guild_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return Guild.parse_obj(result["data"])
        return False

    async def getGuildChannelList(self, guild_id: int, no_cache: bool = False) -> T.Union[list, bool]:
        '''
        获取子频道列表
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_channel_list", {
            "guild_id": guild_id,
            "no_cache": no_cache
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [Channel.parse_obj(_channel) for _channel in result["data"]]
        return False

    async def getGuildMembers(self, guild_id: int) -> T.Union[GuildMembers, bool]:
        '''
        获取频道成员列表
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_members", {
            "guild_id": guild_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return GuildMembers.parse_obj(result["data"])
        return False

    async def sendGuildChannelMessage(self, guild_id: int, channel_id: int, message: T.Union[str, list]) -> T.Union[BotMessage, bool]:
        '''
        发送信息到子频道
        '''
        if isinstance(message, list):
            _message = ""
            for chain in message:
                _message += chain.toString()
            message = _message
        result = await fetch.http_post(f"{self.baseurl_http}/send_guild_channel_msg", {
            "guild_id": guild_id,
            "channel_id": channel_id,
            "message": message
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return BotMessage.parse_obj(result["data"])
        return False

    async def getGuildRoles(self, guild_id: int) -> T.Union[Role, bool]:
        '''
        获取频道身份组列表
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_guild_roles", {
            "guild_id": guild_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [Role.parse_obj(_role) for _role in result["data"]]
        return False

    async def createGuildRole(self, guild_id: int, name: str, color: int, independent: bool, initial_users: T.List[int] = []) -> T.Union[Role, bool]:
        '''
        创建频道身份组
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/create_guild_role", {
            "guild_id": guild_id,
            "name": name,
            "color": color,
            "independent": independent,
            "initial_users": initial_users
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return Role.parse_obj(result["data"])
        return False

    async def deleteGuildRole(self, guild_id: int, role_id: int) -> bool:
        '''
        删除频道身份组
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/delete_guild_role", {
            "guild_id": guild_id,
            "role_id": role_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def setGuildMemberRole(self, guild_id: int, role_id: int, users: T.List[int]) -> bool:
        '''
        设置用户在频道中的身份组
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/set_guild_member_role", {
            "guild_id": guild_id,
            "role_id": role_id,
            "users": users
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def editGuildRole(self, guild_id: int, role_id: int, name: str, color: int, independent: bool) -> bool:
        '''
        设置用户在频道中的身份组
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/update_guild_role", {
            "guild_id": guild_id,
            "role_id": role_id,
            "name": name,
            "color": color,
            "independent": independent # TODO gocq 中参数名写错了，待后续确认
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return True
        return False

    async def getTopicChannelFeeds(self, guild_id: int, channel_id: int) -> T.Union[T.List[TopicChannelFeed], bool]:
        '''
        获取论坛子频道帖子列表
        '''
        result = await fetch.http_post(f"{self.baseurl_http}/get_topic_channel_feeds", {
            "guild_id": guild_id,
            "channel_id": channel_id
        }, params=self.protocol_params)
        if result["status"] == "ok":
            return [TopicChannelFeed.parse_obj(_feed) for _feed in result["data"]]
        return False