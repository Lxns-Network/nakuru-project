import sys
import aiohttp
import asyncio
import inspect
import copy
import pydantic
import traceback

from contextlib import AsyncExitStack
from typing import Callable, NamedTuple, Awaitable, Any, List, Dict
from functools import partial
from async_lru import alru_cache

from .event import InternalEvent, ExternalEvent
from .event.models import MessageTypes, NoticeTypes, RequestTypes, Friend, Member, GuildMember
from .event.builtins import ExecutorProtocol, Depend
from .event.models import (
    FriendMessage, GroupMessage, GuildMessage, MessageItemType
)
from .event.enums import ExternalEvents
from .misc import argument_signature, raiser, TRACEBACKED
from .protocol import CQHTTP_Protocol
from .logger import logger

class CQHTTP(CQHTTP_Protocol):
    event: Dict[
        str, List[Callable[[Any], Awaitable]]
    ] = {}
    lifecycle: Dict[str, List[Callable]] = {
        "start": [],
        "end": [],
        "around": []
    }
    global_dependencies: List[Depend]
    global_middlewares: List

    def __init__(self,
                 host: str = None,
                 port: int = None,
                 http_port: int = None,
                 global_dependencies: List[Depend] = None,
                 global_middlewares: List = None):
        self.global_dependencies = global_dependencies or []
        self.global_middlewares = global_middlewares or []

        self.baseurl = f"http://{host}:{port}"
        self.baseurl_http = f"http://{host}:{http_port}"

    async def ws_event(self):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(f"{self.baseurl}") as ws_connection:
                logger.info("Protocol: connected")
                while True:
                    try:
                        received_data = await ws_connection.receive_json()
                    except TypeError:
                        continue
                    if received_data:
                        post_type = received_data["post_type"]
                        try:
                            if post_type == "message":
                                received_data = MessageTypes[received_data["message_type"]].parse_obj(received_data)
                            elif post_type == "notice":
                                received_data = NoticeTypes[received_data["notice_type"]].parse_obj(received_data)
                            elif post_type == "request":
                                received_data = RequestTypes[received_data["request_type"]].parse_obj(received_data)
                            else:
                                continue
                        except KeyError:
                            logger.error("Protocol: data parse error: " + received_data)
                            continue
                        except pydantic.error_wrappers.ValidationError:
                            logger.error("Protocol: data parse error: " + received_data)
                            continue
                        await self.queue.put(InternalEvent(
                            name=self.getEventCurrentName(type(received_data)),
                            body=received_data
                        ))

    async def event_runner(self):
        while True:
            try:
                event_context: NamedTuple[InternalEvent] = await asyncio.wait_for(self.queue.get(), 3)
            except asyncio.TimeoutError:
                continue

            if event_context.name in self.registeredEventNames:
                logger.info(f"Event: handling a event: {event_context.name}")
                for event_body in list(self.event.values()) \
                        [self.registeredEventNames.index(event_context.name)]:
                    if event_body:
                        running_loop = asyncio.get_running_loop()
                        running_loop.create_task(self.executor(event_body, event_context))

    @property
    def registeredEventNames(self):
        return [self.getEventCurrentName(i) for i in self.event.keys()]

    async def executor(self,
                       executor_protocol: ExecutorProtocol,
                       event_context,
                       extra_parameter={},
                       lru_cache_sets=None
                       ):
        lru_cache_sets = lru_cache_sets or {}
        executor_protocol: ExecutorProtocol
        for depend in executor_protocol.dependencies:
            if not inspect.isclass(depend.func):
                depend_func = depend.func
            elif hasattr(depend.func, "__call__"):
                depend_func = depend.func.__call__
            else:
                raise TypeError("must be callable.")

            if depend_func in lru_cache_sets and depend.cache:
                depend_func = lru_cache_sets[depend_func]
            else:
                if depend.cache:
                    original = depend_func
                    if inspect.iscoroutinefunction(depend_func):
                        depend_func = alru_cache(depend_func)
                    else:
                        depend_func = lru_cache(depend_func)
                    lru_cache_sets[original] = depend_func

            result = await self.executor_with_middlewares(
                depend_func, depend.middlewares, event_context, lru_cache_sets
            )
            if result is TRACEBACKED:
                return TRACEBACKED

        ParamSignatures = argument_signature(executor_protocol.callable)
        PlaceAnnotation = self.get_annotations_mapping()
        CallParams = {}
        for name, annotation, default in ParamSignatures:
            if default:
                if isinstance(default, Depend):
                    if not inspect.isclass(default.func):
                        depend_func = default.func
                    elif hasattr(default.func, "__call__"):
                        depend_func = default.func.__call__
                    else:
                        raise TypeError("must be callable.")

                    if depend_func in lru_cache_sets and default.cache:
                        depend_func = lru_cache_sets[depend_func]
                    else:
                        if default.cache:
                            original = depend_func
                            if inspect.iscoroutinefunction(depend_func):
                                depend_func = alru_cache(depend_func)
                            else:
                                depend_func = lru_cache(depend_func)
                            lru_cache_sets[original] = depend_func

                    CallParams[name] = await self.executor_with_middlewares(
                        depend_func, default.middlewares, event_context, lru_cache_sets
                    )
                    continue
                else:
                    raise RuntimeError("checked a unexpected default value.")
            else:
                if annotation in PlaceAnnotation:
                    CallParams[name] = PlaceAnnotation[annotation](event_context)
                    continue
                else:
                    if name not in extra_parameter:
                        raise RuntimeError(f"checked a unexpected annotation: {annotation}")

        async with AsyncExitStack() as stack:
            sorted_middlewares = self.sort_middlewares(executor_protocol.middlewares)
            for async_middleware in sorted_middlewares['async']:
                await stack.enter_async_context(async_middleware)
            for normal_middleware in sorted_middlewares['normal']:
                stack.enter_context(normal_middleware)

            return await self.run_func(executor_protocol.callable, **CallParams, **extra_parameter)
    
    async def _run(self):
        loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(loop=loop) if sys.version_info.minor < 10 else asyncio.Queue()
        loop.create_task(self.ws_event())
        loop.create_task(self.event_runner())

        await self.queue.put(InternalEvent(
            name=self.getEventCurrentName("AppInitEvent"),
            body={}
        ))
        try:
            for start_callable in self.lifecycle['start']:
                await self.run_func(start_callable, self)

            for around_callable in self.lifecycle['around']:
                await self.run_func(around_callable, self)

        except KeyboardInterrupt:
            logger.info("catched Ctrl-C, exiting..")
        except Exception as e:
            traceback.print_exc()
        finally:
            for around_callable in self.lifecycle['around']:
                await self.run_func(around_callable, self)

            for end_callable in self.lifecycle['end']:
                await self.run_func(end_callable, self)
    
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._run())

    def receiver(self,
                 event_name,
                 dependencies: List[Depend] = None,
                 use_middlewares: List[Callable] = None):
        def receiver_warpper(func: Callable):
            if not inspect.iscoroutinefunction(func):
                raise TypeError("event body must be a coroutine function.")
            
            self.event.setdefault(event_name, [])
            self.event[event_name].append(ExecutorProtocol(
                callable=func,
                dependencies=(dependencies or []) + self.global_dependencies,
                middlewares=(use_middlewares or []) + self.global_middlewares
            ))
            return func

        return receiver_warpper

    def getEventCurrentName(self, event_value):
        class_list = (
            GroupMessage,
            FriendMessage,
            GuildMessage,
            *self.get_event_class_name()
        )
        if inspect.isclass(event_value) and issubclass(event_value, ExternalEvent):  # subclass
            return event_value.__name__
        elif isinstance(event_value, class_list):  # normal class
            return event_value.__class__.__name__
        elif event_value in class_list:  # message
            return event_value.__name__
        elif isinstance(event_value, (  # enum
            MessageItemType,
            ExternalEvents
        )):
            return event_value.name
        else:
            return event_value

    def get_annotations_mapping(self):
        return {
            CQHTTP: lambda k: self,
            FriendMessage: lambda k: k.body \
                if self.getEventCurrentName(k.body) == "FriendMessage" else \
                raiser(ValueError("you cannot setting a unbind argument.")),
            GroupMessage: lambda k: k.body \
                if self.getEventCurrentName(k.body) == "GroupMessage" else \
                raiser(ValueError("you cannot setting a unbind argument.")),
            GuildMessage: lambda k: k.body \
                if self.getEventCurrentName(k.body) == "GuildMessage" else \
                raiser(ValueError("you cannot setting a unbind argument.")),
            Friend: lambda k: k.body.sender \
                if self.getEventCurrentName(k.body) == "FriendMessage" else \
                raiser(ValueError("Friend is not enable in this type of event.")),
            Member: lambda k: k.body.sender \
                if self.getEventCurrentName(k.body) == "GroupMessage" else \
                raiser(ValueError("Group is not enable in this type of event.")),
            GuildMember: lambda k: k.body.sender \
                if self.getEventCurrentName(k.body) == "GuildMessage" else \
                raiser(ValueError("Group is not enable in this type of event.")),
            "Sender": lambda k: k.body.sender \
                if self.getEventCurrentName(k.body) in MessageTypes else \
                raiser(ValueError("Sender is not enable in this type of event.")),
            "Type": lambda k: self.getEventCurrentName(k.body),
            **self.gen_event_anno()
        }

    def get_event_class_name(self):
        def warpper(name, event_context):
            if name != event_context.name:
                raise ValueError("cannot look up a non-listened event.")
            return event_context.body
        
        return {
            event_class.value for event_name, event_class in ExternalEvents.__members__.items()
        }

    def gen_event_anno(self):
        def warpper(name, event_context):
            if name != event_context.name:
                raise ValueError("cannot look up a non-listened event.")
            return event_context.body
        
        return {
            event_class.value: partial(warpper, copy.copy(event_name)) \
            for event_name, event_class in ExternalEvents.__members__.items()
        }

    @staticmethod
    def sort_middlewares(iterator):
        return {
            "async": [
                i for i in iterator if all([
                    hasattr(i, "__aenter__"),
                    hasattr(i, "__aexit__")
                ])
            ],
            "normal": [
                i for i in iterator if all([
                    hasattr(i, "__enter__"),
                    hasattr(i, "__exit__")
                ])
            ]
        }

    @staticmethod
    async def run_func(func, *args, **kwargs):
        if inspect.iscoroutinefunction(func):
            await func(*args, **kwargs)
        else:
            func(*args, **kwargs)
