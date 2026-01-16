from typing import List, Union

import hikari

from bobert.core.utils import constants as const

badge_emoji_mapping = {
    hikari.UserFlag.BUG_HUNTER_LEVEL_1: const.EMOJI_BUGHUNTER,
    hikari.UserFlag.BUG_HUNTER_LEVEL_2: const.EMOJI_BUGHUNTER_GOLD,
    hikari.UserFlag.DISCORD_CERTIFIED_MODERATOR: const.EMOJI_CERTIFIED_MOD,
    hikari.UserFlag.EARLY_SUPPORTER: const.EMOJI_EARLY_SUPPORTER,
    hikari.UserFlag.EARLY_VERIFIED_DEVELOPER: const.EMOJI_VERIFIED_DEVELOPER,
    hikari.UserFlag.HYPESQUAD_EVENTS: const.EMOJI_HYPESQUAD_EVENTS,
    hikari.UserFlag.HYPESQUAD_BALANCE: const.EMOJI_HYPESQUAD_BALANCE,
    hikari.UserFlag.HYPESQUAD_BRAVERY: const.EMOJI_HYPESQUAD_BRAVERY,
    hikari.UserFlag.HYPESQUAD_BRILLIANCE: const.EMOJI_HYPESQUAD_BRILLIANCE,
    hikari.UserFlag.PARTNERED_SERVER_OWNER: const.EMOJI_PARTNER,
    hikari.UserFlag.DISCORD_EMPLOYEE: const.EMOJI_PARTNER,
    hikari.UserFlag.VERIFIED_BOT: const.EMOJI_VERIFIED_BOT,
}


def get_badges(user: hikari.User) -> List[str]:
    return [emoji for flag, emoji in badge_emoji_mapping.items() if flag & user.flags]
