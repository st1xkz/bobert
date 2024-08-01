from __future__ import annotations

import typing as t
from typing import Union

if t.TYPE_CHECKING:
    from hikari import Member, User

ORDINAL_ENDINGS: t.Final = {"1": "st", "2": "nd", "3": "rd"}


def list_of(items: list[str], sep: str = "and") -> str:
    if len(items) > 2:
        return f"{', '.join(items[:-1])}, {sep} {items[-1]}"

    return f" {sep} ".join(items)


def ordinal(number: int) -> str:
    if str(number)[-2:] not in ("11", "12", "13"):
        return f"{number:,}{ORDINAL_ENDINGS.get(str(number)[-1], 'th')}"

    return f"{number:,}th"


def possessive(user: Union[Member, User]) -> str:
    name = getattr(user, "display_name", user.username)
    return f"{name}'{'s' if not name.endswith('s') else ''}"
