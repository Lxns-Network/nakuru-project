import json
import mimetypes
import typing as T
from pathlib import Path
from .logger import logger

import aiohttp

class fetch:
    @staticmethod
    async def http_post(url, data_map=None):
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data_map) as response:
                data = await response.text(encoding="utf-8")
                logger.debug("Network: ", f"requested url={url}, by data_map={data_map}, and status={response.status}, data={data}")
                response.raise_for_status()
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.error("Network: ", f"requested {url} with {data_map}, responsed {data}, decode failed...")

    @staticmethod
    async def http_get(url, params=None): 
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.text(encoding="utf-8")
                logger.debug("Network: ", f"requested url={url}, by params={params}, and status={response.status}, data={data}")
        try:
            return json.loads(data)
        except json.decoder.JSONDecodeError:
            logger.error("Network: ", f"requested {url} with {params}, responsed {data}, decode failed...")
