import inspect
import os
import typing as T
from collections import namedtuple

from .logger import Protocol

Parameter = namedtuple("Parameter", ["name", "annotation", "default"])

TRACEBACKED = os.urandom(32)


def raiser(error):
    raise error


def protocol_log(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            Protocol.info(f"protocol method {func.__name__} was called")
            return result
        except Exception as e:
            Protocol.error(f"protocol method {func.__name__} raised a error: {e.__class__.__name__}")
            raise e

    return wrapper


def argument_signature(callable_target) -> T.List[Parameter]:
    return [
        Parameter(
            name=name,
            annotation=param.annotation if param.annotation != inspect._empty else None,
            default=param.default if param.default != inspect._empty else None
        )
        for name, param in dict(inspect.signature(callable_target).parameters).items()
    ]


import re
from .entities.components import ComponentTypes


class CQParser:
    def __replaceChar(self, string, char, start, end):
        string = list(string)
        del (string[start:end])
        string.insert(start, char)
        return ''.join(string)

    # 获得文本中每一个 CQ 码的起始和结束位置
    def __getCQIndex(self, text):
        cqIndex = []
        for m in re.compile("(\[CQ:(.+?)])").finditer(text):
            cqIndex.append((m.start(), m.end()))
        cqIndex.append((len(text), len(text)))
        return cqIndex

    # 转义中括号
    def escape(self, text, isEscape=True):
        if isEscape:
            text = text.replace("&", "&amp;")
            text = text.replace(",", "&#44;")
            text = text.replace("[", "&#91;")
            text = text.replace("]", "&#93;")
        else:
            text = text.replace("&amp;", "&")
            text = text.replace("&#44;", ",")
            text = text.replace("&#91;", "[")
            text = text.replace("&#93;", "]")
        return text

    # 将纯文本转换成类型为 plain 的 CQ 码
    def plainToCQ(self, text):
        i = j = k = 0
        cqIndex = self.__getCQIndex(text)
        while i < len(cqIndex):
            if i > 0:
                if i == 1:
                    k += 1
                else:
                    j += 1
            cqIndex = self.__getCQIndex(text)
            if i > 0:
                l, r = cqIndex[j][k], cqIndex[j + 1][0]
            else:
                l, r = 0, cqIndex[0][0]
            source_text = text[l:r]
            if source_text != "":
                text = self.__replaceChar(text, f"[CQ:plain,text={self.escape(source_text)}]", l, r)
            i += 1
        return text

    def getAttributeList(self, text):
        text_array = text.split(",")
        text_array.pop(0)
        attribute_list = {}
        for _ in text_array:
            regex_result = re.search(r"^(.*?)=([\s\S]+)", _)
            k = regex_result.group(1)
            if k == "type":
                k = "_type"
            v = self.escape(regex_result.group(2), isEscape=False)
            attribute_list[k] = v
        return attribute_list

    def parseChain(self, text):
        text = self.plainToCQ(text)
        cqcode_list = re.findall(r'(\[CQ:([\s\S]+?)])', text)
        chain = []
        for x in cqcode_list:
            message_type = re.search(r"^\[CQ\:(.*?)\,", x[0]).group(1)
            try:
                chain.append(ComponentTypes[message_type].parse_obj(self.getAttributeList(x[1])))
            except:
                chain.append(ComponentTypes["unknown"].parse_obj({"text": message_type}))
                Protocol.error(f"Cannot convert message type: {message_type}")
        return chain
