from __future__ import annotations

import random
import io
from dataclasses import asdict

import aiofiles
from aiofiles.threadpool.binary import AsyncBufferedReader

from .http import _HTTPClient
from .cache import _Cache
from .utils import FileNotUploaded, _DataDict, _open_image

__all__ = ("Duck",)


class Duck(_HTTPClient, _Cache):
    """
    The main client class.
    """

    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Quack"
    
    def __repr__(self) -> str:
        return "Quack Quack"

    async def fetch_random(self, *, gif: bool = False, jpg: bool = False) -> str:
        """
        Fetches a random jpg link or a gif link from the API, if the type of link isn't specified then the API will randomly return either a jpg or a gif url.
        Note that since there's a lot more jpgs than gifs in the api, jpgs will get returned more frequently.

        Parameters
        ----------
        gif : :class:`Optional[bool]`
            Whether to fetch only gif from the API, default is set to ``False``.
        jpg : :class:`Optional[bool]`
            Whether to fetch only jpg from the API, default is set to ``False``.

        Returns
        -------
        :class:`str`
        """
        if gif:
            data: str = (await self._request("random", query="?type=gif"))["url"]
            if not self._cache.get("gifs"):
                self._cache["gifs"] = [data]
            else:
                self._cache["gifs"].append(data)
        elif jpg:
            data = (await self._request("random", query="?type=jpg"))["url"]
            if not self._cache.get("jpgs"):
                self._cache["jpgs"] = [data]
            else:
                self._cache["jpgs"].append(data)
        else:
            data = (await self._request("random"))["url"]
            if "gif" in data:
                if not self._cache.get("gifs"):
                    self._cache["gifs"] = [data]
                else:
                    self._cache["gifs"].append(data)
            else:
                if not self._cache.get("jpgs"):
                    self._cache["jpgs"] = [data]
                else:
                    self._cache["jpgs"].append(data)

        return data

    async def fetch_random_file(
        self, *, gif: bool = False, jpg: bool = False
    ) -> io.BytesIO:
        """
        Fetches a random jpg file or a gif file from the API, if the type of file isn't specified then the API will randomly return either a jpg or a gif file.
        Note that since there's a lot more jpgs than gifs in the api, jpgs will get returned more frequently.

        Parameters
        ----------
        gif: :class:`Optional[bool]`
            Whether to fetch only gif from the API, default is set to ``False``.

        jpg: :class:`Optional[bool]`
            Whether to fetch only jpg from the API, default is set to ``False``.

        Returns
        -------
        :class:`io.BytesIO`
        """
        if gif:
            data: bytes = await self._request(
                "randomimg", query="?type=gif", image=True
            )
            if not self._cache.get("gifs"):
                self._cache["gifs"] = [data]
            else:
                self._cache["gifs"].append(data)
        elif jpg:
            data = await self._request("randomimg", query="?type=jpg", image=True)
            if not self._cache.get("jpgs"):
                self._cache["jpgs"] = [data]
            else:
                self._cache["jpgs"].append(data)
        else:
            data = await self._request("randomimg", image=True)
            if not self._cache.get("random_images"):
                self._cache["random_images"] = [data]
            else:
                self._cache["random_images"].append(data)

        img: io.BytesIO = await _open_image(data)
        return img

    async def fetch_list(
        self, *, gif: bool = False, jpg: bool = False, http: bool = False
    ) -> dict[str, list[str] | int] | list[str]:
        """
        A method to get a specific list from the API, if no list is specified then everything is returned.

        Parameters
        ----------
        gif: :class:`Optional[bool]`
            Whether to only get the gif list of the dict.

        jpg: :class:`Optional[bool]`
            Whether to only get the jpg list of the dict.

        http: :class:`Optional[bool]`
            Whether to only get the http list of the dict.

        Returns
        -------
        :class:`dict[str, list[str] | int] | list[str]`
        """
        data = asdict(_DataDict(**(await self._request("list"))))

        if gif:
            gif_data: list[str] = data["gifs"]
            gif_data.sort(key=lambda v: int(v.split(".")[0]))
            return gif_data
        elif jpg:
            jpg_data: list[str] = data["images"]
            jpg_data.sort(key=lambda v: int(v.split(".")[0]))
            return jpg_data
        elif http:
            http_data: list[str] = data["http"]
            http_data.sort(key=lambda v: int(v.split(".")[0]))
            return http_data

        return data

    async def fetch_jpg(self, jpg: int, /) -> io.BytesIO:
        """
        Fetches a specified jpg from the API.

        Parameters
        ----------
        jpg: :class:`int`
            The jpg to fetch.

        Returns
        -------
        :class:`io.BytesIO`
        """
        data: bytes = await self._request(f"{jpg}.jpg", image=True)
        img = await _open_image(data)
        if not self._cache.get("jpgs"):
            self._cache["jpgs"] = [img]
        else:
            self._cache["jpgs"].append(img)

        return img

    async def fetch_gif(self, gif: int, /) -> io.BytesIO:
        """
        Fetches a specified gif from the API.

        Parameters
        ----------
        gif: :class:`int`
            The gif to fetch.

        Returns
        -------
        :class:`io.BytesIO`
        """
        data: bytes = await self._request(f"{gif}.gif", image=True)
        img = await _open_image(data)
        if not self._cache.get("gifs"):
            self._cache["gifs"] = [img]
        else:
            self._cache["gifs"].append(img)

        return img

    async def fetch_http(self, code: int, /) -> io.BytesIO:
        """
        Fetches a specified http from the API.

        Parameters
        ----------
        code: :class:`int`
            The http image to fetch

        Returns
        -------
        :class:`io.BytesIO`
        """
        data: bytes = await self._request(f"http/{code}", image=True)
        img: io.BytesIO = await _open_image(data)
        if not self._cache.get("https"):
            self._cache["https"] = [img]
        else:
            self._cache["https"].append(img)

        return img

    async def upload(
        self, file: str | io.IOBase | AsyncBufferedReader, /
    ) -> str | None:
        """
        Upload a duck image to the API, note that image extension must be either jpg, gif, png, or bmp.

        Parameters
        ----------
        file: :class:`Union[str, io.IOBase, AsyncBufferedReader]`
            The file to upload

        Returns
        -------
        :class:`Optional[str]`
        """
        if isinstance(file, str):
            async with aiofiles.open(file, "rb") as f:
                file_to_upload: io.RawIOBase = f.raw

        elif isinstance(file, (io.BufferedReader, AsyncBufferedReader)):
            file_to_upload = file.raw

        else:
            raise TypeError(f"Expected str or a file object, not {type(file).__name__}")
        data: str | None = await self._post_request(file={"file": file_to_upload})
        return data
