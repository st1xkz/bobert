from __future__ import annotations

import io

__all__ = ("_Cache",)


class _Cache:
    def __init__(self) -> None:
        self._cache: dict[str, list[str | io.BytesIO | bytes]] = {}
    
    def __iter__(self) -> dict[str, list[str | io.BytesIO | bytes]]:
        self._cache

    @property
    async def gif_cache(self) -> list[str | io.BytesIO | bytes] | None:
        """
        Returns the gif list from the cache, if there isn't any gif cached it returns none.

        Returns
        -------
        Optional[List[Union[:class:`str`, :class:`io.BytesIO`, :class:`bytes`]]
        """
        return self._cache.get("gifs")

    @property
    async def http_cache(self) -> list[str | io.BytesIO | bytes] | None:
        """
        Returns the http list from the cache, if there isn't any http cached yet it returns none.

        Returns
        -------
        Optional[List[Union[:class:`str`, :class:`io.BytesIO`, :class:`bytes`]]
        """
        return self._cache.get("https")

    @property
    async def jpg_cache(self) -> list[str | io.BytesIO | bytes] | None:
        """
        Returns the jpg list from the cache, if there isn't any jpg it returns none.

        Returns
        -------
        Optional[List[Union[:class:`str`, :class:`io.BytesIO`, :class:`bytes`]]
        """
        return self._cache.get("jpgs")

    @property
    async def get_cache(self) -> dict[str, list[str | io.BytesIO | bytes]]:
        """
        Gets the entire cache.

        Returns
        -------
        Dict[:class:`str`, List[Union[:class:`str`, :class:`io.BytesIO`, :class:`bytes`]]]
        """
        return self._cache
