from typing import Sequence

import hikari


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)
