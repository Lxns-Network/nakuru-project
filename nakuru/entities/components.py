from pydantic import BaseModel
from enum import Enum
import typing as T
import json
import os

from ..logger import Protocol

class ComponentType(Enum):
    Plain = "Plain"
    Face = "Face"
    Record = "Record"
    Video = "Video"
    At = "At"
    RPS = "RPS" # TODO
    Dice = "Dice" # TODO
    Shake = "Shake" # TODO
    Anonymous = "Anonymous" # TODO
    Share = "Share"
    Contact = "Contact" # TODO
    Location = "Location" # TODO
    Music = "Music"
    Image = "Image"
    Reply = "Reply"
    RedBag = "RedBag"
    Poke = "Poke"
    Gift = "Gift"
    Forward = "Forward"
    Node = "Node"
    Xml = "Xml"
    Json = "Json"
    CardImage = "CardImage"
    TTS = "TTS"
    Unknown = "Unknown"

class BaseMessageComponent(BaseModel):
    type: ComponentType

    def toString(self):
        output = f"[CQ:{self.type.lower()}"
        for k, v in self.__dict__.items():
            if k == "type" or v is None:
                continue
            if k == "_type":
                k = "type"
            if isinstance(v, bool):
                v = 1 if v else 0
            output += ",%s=%s" % (k, str(v).replace("&", "&amp;")\
                                           .replace(",", "&#44;")\
                                           .replace("[", "&#91;")\
                                           .replace("]", "&#93;"))
        output += "]"
        return output
    
    def toDict(self):
        data = dict()
        for k, v in self.__dict__.items():
            if k == "type" or v is None:
                continue
            if k == "_type":
                k = "type"
            data[k] = v
        return {
            "type": self.type.lower(),
            "data": data
        }

class Plain(BaseMessageComponent):
    type: ComponentType = "Plain"
    text: str

    def __init__(self, text: str, **_):
        super().__init__(text=text, **_)

    def toString(self): # 没有 [CQ:plain] 这种东西，所以直接导出纯文本
        return self.text.replace("&", "&amp;")\
                        .replace(",", "&#44;")\
                        .replace("[", "&#91;")\
                        .replace("]", "&#93;")

class Face(BaseMessageComponent):
    type: ComponentType = "Face"
    id: int

    def __init__(self, **_):
        super().__init__(**_)

class Record(BaseMessageComponent):
    type: ComponentType = "Record"
    file: T.Optional[str]
    magic: T.Optional[bool] = False
    url: T.Optional[str]
    cache: T.Optional[bool] = True
    proxy: T.Optional[bool] = True
    timeout: T.Optional[int] = 0

    def __init__(self, file: T.Optional[str], **_):
        for k in _.keys():
            if k == "url":
                Protocol.warn(f"go-cqhttp doesn't support send {self.type} by {k}")
        super().__init__(file=file, **_)
    
    @staticmethod
    def fromFileSystem(path, **_):
        return Record(file=f"file:///{os.path.abspath(path)}", **_)

class Video(BaseMessageComponent):
    type: ComponentType = "Video"
    file: str
    cover: T.Optional[str]
    c: T.Optional[int] = 2

    def __init__(self, file: str, **_):
        for k in _.keys():
            if k == "c" and _[k] not in [2, 3]:
                Protocol.warn(f"{k}={_[k]} doesn't match values")
        super().__init__(file=file, **_)
    
    @staticmethod
    def fromFileSystem(path, **_):
        return Video(file=f"file:///{os.path.abspath(path)}", **_)

class At(BaseMessageComponent):
    type: ComponentType = "At"
    qq: int
    name: T.Optional[str]

    def __init__(self, **_):
        super().__init__(**_)

class RPS(BaseMessageComponent): # TODO
    type: ComponentType = "RPS"

    def __init__(self, **_):
        super().__init__(**_)

class Dice(BaseMessageComponent): # TODO
    type: ComponentType = "Dice"

    def __init__(self, **_):
        super().__init__(**_)

class Shake(BaseMessageComponent): # TODO
    type: ComponentType = "Shake"

    def __init__(self, **_):
        super().__init__(**_)

class Anonymous(BaseMessageComponent): # TODO
    type: ComponentType = "Anonymous"
    ignore: T.Optional[bool]

    def __init__(self, **_):
        super().__init__(**_)

class Share(BaseMessageComponent):
    type: ComponentType = "Share"
    url: str
    title: str
    content: T.Optional[str]
    image: T.Optional[str]

    def __init__(self, **_):
        super().__init__(**_)

class Contact(BaseMessageComponent): # TODO
    type: ComponentType = "Contact"
    _type: str # type 字段冲突
    id: T.Optional[int]

    def __init__(self, **_):
        for k in _.keys():
            if k == "_type" and _[k] not in ["qq", "group"]:
                Protocol.warn(f"{k}={_[k]} doesn't match values")
        super().__init__(**_)

class Location(BaseMessageComponent): # TODO
    type: ComponentType = "Location"
    lat: float
    lon: float
    title: T.Optional[str]
    content: T.Optional[str]

    def __init__(self, **_):
        super().__init__(**_)

class Music(BaseMessageComponent):
    type: ComponentType = "Music"
    _type: str
    id: T.Optional[int]
    url: T.Optional[str]
    audio: T.Optional[str]
    title: T.Optional[str]
    content: T.Optional[str]
    image: T.Optional[str]

    def __init__(self, **_):
        for k in _.keys():
            if k == "_type" and _[k] not in ["qq", "163", "xm", "custom"]:
                Protocol.warn(f"{k}={_[k]} doesn't match values")
        super().__init__(**_)

class Image(BaseMessageComponent):
    type: ComponentType = "Image"
    file: T.Optional[str]
    _type: T.Optional[str]
    subType: T.Optional[int]
    url: T.Optional[str]
    cache: T.Optional[bool] = True
    id: T.Optional[int] = 40000
    c: T.Optional[int] = 2

    def __init__(self, file: T.Optional[str], **_):
        for k in _.keys():
            if (k == "_type" and _[k] not in ["flash", "show", None]) or \
                    (k == "c" and _[k] not in [2, 3]):
                Protocol.warn(f"{k}={_[k]} doesn't match values")
        super().__init__(file=file, **_)
    
    @staticmethod
    def fromFileSystem(path, **_):
        return Image(file=f"file:///{os.path.abspath(path)}", **_)

class Reply(BaseMessageComponent):
    type: ComponentType = "Reply"
    id: int
    text: T.Optional[str]
    qq: T.Optional[int]
    time: T.Optional[int]
    seq: T.Optional[int]

    def __init__(self, **_):
        super().__init__(**_)

class RedBag(BaseMessageComponent):
    type: ComponentType = "RedBag"
    title: str

    def __init__(self, **_):
        super().__init__(**_)

class Poke(BaseMessageComponent):
    type: ComponentType = "Poke"
    qq: int

    def __init__(self, **_):
        super().__init__(**_)

class Gift(BaseMessageComponent):
    type: ComponentType = "Gift"
    qq: int
    id: int

    def __init__(self, **_):
        super().__init__(**_)

class Forward(BaseMessageComponent):
    type: ComponentType = "Forward"
    id: str

    def __init__(self, **_):
        super().__init__(**_)

class Node(BaseMessageComponent): # 该 component 仅支持使用 sendGroupForwardMessage 发送
    type: ComponentType = "Node"
    id: T.Optional[int]
    name: T.Optional[str]
    uin: T.Optional[int]
    content: T.Optional[T.Union[str, list]]
    seq: T.Optional[T.Union[str, list]] # 不清楚是什么
    time: T.Optional[int]

    def __init__(self, content: T.Union[str, list], **_):
        if isinstance(content, list):
            _content = ""
            for chain in content:
                _content += chain.toString()
            content = _content
        super().__init__(content=content, **_)
    
    def toString(self):
        Protocol.warn(f"node doesn't support stringify")
        return ""

class Xml(BaseMessageComponent):
    type: ComponentType = "Xml"
    data: str
    resid: T.Optional[int]

    def __init__(self, **_):
        super().__init__(**_)

class Json(BaseMessageComponent):
    type: ComponentType = "Json"
    data: T.Union[str, dict]
    resid: T.Optional[int] = 0

    def __init__(self, data, **_):
        if isinstance(data, dict):
            data = json.dumps(data)
        super().__init__(data=data, **_)

class CardImage(BaseMessageComponent):
    type: ComponentType = "CardImage"
    file: str
    cache: T.Optional[bool] = True
    minwidth: T.Optional[int] = 400
    minheight: T.Optional[int] = 400
    maxwidth: T.Optional[int] = 500
    maxheight: T.Optional[int] = 500
    source: T.Optional[str]
    icon: T.Optional[str]

    def __init__(self, **_):
        super().__init__(**_)
    
    @staticmethod
    def fromFileSystem(path, **_):
        return CardImage(file=f"file:///{os.path.abspath(path)}", **_)

class TTS(BaseMessageComponent):
    type: ComponentType = "TTS"
    text: str

    def __init__(self, **_):
        super().__init__(**_)

class Unknown(BaseMessageComponent):
    type: ComponentType = "Unknown"
    text: str

    def toString(self):
        return ""

ComponentTypes = {
    "plain": Plain,
    "face": Face,
    "record": Record,
    "video": Video,
    "at": At,
    "rps": RPS,
    "dice": Dice,
    "shake": Shake,
    "anonymous": Anonymous,
    "share": Share,
    "contact": Contact,
    "location": Location,
    "music": Music,
    "image": Image,
    "reply": Reply,
    "redbag": RedBag,
    "poke": Poke,
    "gift": Gift,
    "forward": Forward,
    "node": Node,
    "xml": Xml,
    "json": Json,
    "cardimage": CardImage,
    "tts": TTS,
    "unknown": Unknown
}