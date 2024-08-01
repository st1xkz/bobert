from __future__ import annotations

import typing

import hikari
import lightbulb

from bobert.core.stuff.badges import *
from bobert.core.utils import constants as const
from bobert.core.utils import format_dt, helpers

context = lightbulb.Plugin("context")


def mutual_guilds(bot: hikari.GatewayBot, member: hikari.Member) -> list[hikari.Guild]:
    all_members = bot.cache.get_members_view()
    return [
        guild
        for guild in (
            bot.cache.get_guild(guild_id)
            for guild_id, members in all_members.items()
            if member.id in members
        )
        if guild is not None
    ]


def get_status(activity: typing.Optional[hikari.Activity]) -> str:
    if activity is None:
        return "No Activity"

    type_ = activity.type
    name = "Unknown Activity"

    if type_ is hikari.ActivityType.CUSTOM:
        return str(activity.state)
    elif type_ is hikari.ActivityType.WATCHING:
        name = "Watching"
    elif type_ is hikari.ActivityType.LISTENING:
        name = "Listening to"
    elif type_ is hikari.ActivityType.STREAMING:
        name = "Streaming"
    elif type_ is hikari.ActivityType.PLAYING:
        name = "Playing"
    elif type_ is hikari.ActivityType.COMPETING:
        name = "Competing in"

    return f"{name} **{activity.name}**"


@context.command
@lightbulb.command(
    name="Show who-is",
    description="Displays member information",
)
@lightbulb.implements(lightbulb.UserCommand)
async def show_user_ctx(ctx: lightbulb.UserContext) -> None:
    target = ctx.bot.cache.get_member(ctx.guild_id, ctx.options.target.id)  # type: ignore

    if target is None:
        await ctx.respond(
            "❌ The user you specified isn't in the server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    roles = helpers.sort_roles(target.get_roles())
    color = next((r.color for r in roles if r.color), None)

    roles_mentions = [role.mention for role in roles if role.id != ctx.guild_id]
    roles = ", ".join(roles_mentions) if roles_mentions else "No roles"

    role_num = (await target.fetch_roles())[1:]

    guild = ctx.get_guild()
    if guild is None:
        await ctx.respond(
            "❌ Could not retrieve the guild information.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    members = guild.get_members()
    if members is None:
        await ctx.respond(
            "❌ Could not retrieve the member list.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    member_count = (
        len(
            [
                m
                for m in members.values()
                if m.joined_at is not None
                and target.joined_at is not None
                and m.joined_at < target.joined_at
            ]
        )
        + 1
    )

    presence = target.get_presence()

    if presence is not None:
        visible_status = presence.visible_status.lower()

        if visible_status == "online":
            status_emoji = const.EMOJI_ONLINE
        elif visible_status == "idle":
            status_emoji = const.EMOJI_IDLE
        elif visible_status == "dnd":
            status_emoji = const.EMOJI_DND
        else:
            status_emoji = const.EMOJI_OFFLINE
    else:
        status_emoji = const.EMOJI_OFFLINE

    if presence and presence.activities:
        activity = presence.activities[0]
    else:
        activity = None

    if ctx.member is None:
        await ctx.respond(
            "❌ Unable to fetch your member information.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    joined_at_str = (
        f"{format_dt(target.joined_at)} ({format_dt(target.joined_at, style='R')})"
        if target.joined_at is not None
        else "Unknown join date"
    )

    embed = (
        hikari.Embed(
            title=(
                f"{status_emoji} {target.username} ~ {target.nickname}"
                if target.nickname
                else f"{status_emoji} {target.username}"
            ),
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
            get_status(activity) if not isinstance(activity, str) else activity,
            inline=False,
        )
        .add_field(
            "Account Created",
            f"{format_dt(target.created_at)} ({format_dt(target.created_at, style='R')})",
            inline=False,
        )
        .add_field(
            "Joined",
            joined_at_str,
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
            target.display_avatar_url,
        )
        .set_footer(
            text=f"Member #{member_count} | UID: {target.id}",
        )
    )
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@context.command
@lightbulb.command(
    name="Show avatar",
    description="Shows your own or another user's avatar",
)
@lightbulb.implements(lightbulb.UserCommand)
async def show_avatar_ctx(ctx: lightbulb.UserContext) -> None:
    target = ctx.bot.cache.get_member(ctx.guild_id, ctx.options.target.id)  # type: ignore

    if not target:
        await ctx.respond(
            "❌ The user you specified isn't in the server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    color = (
        c[0]
        if (c := [r.color for r in helpers.sort_roles(target.get_roles()) if r.color])
        else None
    )

    at = "Server" if target.guild_avatar_url else "Global"

    embed = hikari.Embed(
        title=f"{target}",
        description=f"[**{at} Avatar URL**]({target.display_avatar_url})",
        color=color,
    )
    embed.set_image(target.display_avatar_url)
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(context)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(context)
