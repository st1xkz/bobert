from __future__ import annotations

import io
from dataclasses import dataclass

__all__ = (
    "_DataDict",
    "BaseException",
    "FileNotUploaded",
    "CouldNotConnect",
    "NotFound",
)

@dataclass
class _DataDict:
    gif_count: int
    gifs: list[str]
    http: list[str]
    image_count: int
    images: list[str]


async def _open_image(data: bytes) -> io.BytesIO:
    img = io.BytesIO(data)
    return img


class BaseException(Exception):
    """
    The base exception class for all of the other exceptions.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class FileNotUploaded(BaseException):
    """
    Raised when there's a problem with uploading a file to the ``add`` endpoint.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CouldNotConnect(BaseException):
    """
    Raised when there's a problem with connecting to the API.
    """
    def __init__(self, status: int) -> None:
        message = f"Could Not Connect to the API. Response status: {status}"
        super().__init__(message)


class NotFound(BaseException):
    """
    Raised when API response status returns 404.
    """
    def __init__(self) -> None:
        message = "404 not found"
        super().__init__(message)
