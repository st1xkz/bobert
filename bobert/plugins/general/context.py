from __future__ import annotations

from datetime import datetime
from typing import Sequence

import hikari
import lightbulb

from bobert.core.stuff.badges import *
from bobert.core.utils import constants as const
from bobert.core.utils import format_dt

context = lightbulb.Plugin("context")


def mutual_guilds(bot: hikari.GatewayBot, member: hikari.Member) -> list[hikari.Guild]:
    all_members = bot.cache.get_members_view()
    return [
        bot.cache.get_guild(guild) for guild, m in all_members.items() if member.id in m
    ]


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)


def get_status(activity: hikari.Activity) -> str:
    type_ = activity.type
    if type_ is hikari.Activity.CUSTOM:
        name = ""
    elif type_ is hikari.Activity.WATCHING:
        name = "Watching"
    elif type_ is hikari.Activity.LISTENING:
        name = "Listening to"
    elif type_ is hikari.Activity.STREAMING:
        name = "Streaming"
    elif type_ is hikari.Activity.PLAYING:
        name = "Playing"
    elif type_ is hikari.Activity.COMPETING:
        name = "Competing in"

    return f"{name} **{activity.name}**"


@context.command
@lightbulb.command(
    name="Show who-is",
    description="Displays member information",
)
@lightbulb.implements(lightbulb.UserCommand)
async def show_user(ctx: lightbulb.UserContext) -> None:
    target = context.bot.cache.get_member(ctx.guild_id, ctx.options.target.id)

    member = target
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    roles = [role.mention for role in sort_roles(target.get_roles())]
    roles.remove(f"<@&{ctx.guild_id}>")
    roles = ", ".join(roles) if roles else "No roles"
    role_num = (await target.fetch_roles())[1:]

    guild = ctx.get_guild()
    member_count = (
        len([m for m in guild.get_members().values() if m.joined_at < target.joined_at])
        + 1
    )

    status_emoji = const.EMOJI_OFFLINE
    if target.get_presence():
        if target.get_presence().visible_status == "online":
            status_emoji = const.EMOJI_ONLINE
        elif target.get_presence().visible_status.lower() == "idle":
            status_emoji = const.EMOJI_IDLE
        elif target.get_presence().visible_status.lower() == "dnd":
            status_emoji = const.EMOJI_DND

    embed = (
        hikari.Embed(
            title=f"{status_emoji} {target.username}#{target.discriminator} ~ {target.nickname}"
            if target.nickname
            else f"{status_emoji} {target.username}",
            description=f"{len(mutual_guilds(ctx.bot, ctx.member))} mutual servers.",
            color=color,
        )
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Boosted?",
            f"{target.premium_since}",
            inline=True,
        )
        .add_field(
            "Activity",
            f"{get_status(activity)}",
            inline=False,
        )
        .add_field(
            "Account Created",
            f"{format_dt(target.created_at)} ({format_dt(target.created_at, style='R')})",
            inline=False,
        )
        .add_field(
            "Joined",
            f"{format_dt(target.joined_at)} ({format_dt(target.joined_at, style='R')})",
            inline=False,
        )
        .add_field(
            f"Roles [{len(role_num)}]",
            f"{roles}",
            inline=False,
        )
        .add_field(
            "Badges",
            f"{'  '.join(get_badges(target)) or 'None'}",
            inline=False,
        )
        .set_thumbnail(
            target.avatar_url or target.default_avatar_url,
        )
        .set_footer(
            text=f"Member #{member_count} | User ID: {target.id}",
        )
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@context.command
@lightbulb.command(
    name="Show avatar",
    description="Shows your own or another user's avatar",
)
@lightbulb.implements(lightbulb.UserCommand)
async def show_avatar(ctx: lightbulb.UserContext) -> None:
    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)

    member = target
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    embed = hikari.Embed(
        title=f"Avatar URL",
        url=f"{target.guild_avatar_url or target.default_avatar_url}",
        color=color,
    )
    embed.set_author(name=f"{ctx.user}")
    embed.set_image(target.guild_avatar_url or target.default_avatar_url)
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(context)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(context)
