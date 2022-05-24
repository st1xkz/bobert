from __future__ import annotations

import asyncio
import io
from typing import Any, ClassVar, Optional

from aiohttp import ClientSession
from aiofiles.threadpool.binary import AsyncBufferedReader

from .utils import FileNotUploaded, CouldNotConnect, NotFound

__all__ = ("_HTTPClient",)


class _HTTPClient:
    """
    Class which deals with all the Requests made to the API.
    """

    _BASEURL: ClassVar[str] = "https://random-d.uk/api/v2/"
    _POSTURL: ClassVar[str] = "https://random-d.uk/add?format=json"

    async def _request(
        self, endpoint: str, query: str = "", image: bool = False
    ) -> Any:
        async with ClientSession() as session:
            async with session.get(f"{self._BASEURL}{endpoint}{query}") as resp:
                if resp.status == 200:
                    if image:
                        return await resp.read()

                    return await resp.json()
                elif resp.status == 404:
                    raise NotFound
                else:
                    raise CouldNotConnect(resp.status)

    async def _post_request(
        self, file: dict[str, io.IOBase | AsyncBufferedReader]
    ) -> str | None:
        async with ClientSession().post(self._POSTURL, data=file) as resp:
            if resp.status == 200:
                data = await resp.json()
                data_message: str = data["message"]
                if not data["success"]:
                    raise FileNotUploaded(data_message)
                return data_message
            else:
                raise CouldNotConnect(resp.status)
