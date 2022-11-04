from __future__ import annotations

from datetime import datetime
from typing import Sequence

import hikari
import lightbulb

from bobert.core.stuff.badges import *
from bobert.core.utils import format_dt

user = lightbulb.Plugin("user")


def mutual_guilds(bot: hikari.GatewayBot, member: hikari.Member) -> list[hikari.Guild]:
    all_members = bot.cache.get_members_view()
    return [
        bot.cache.get_guild(guild) for guild, m in all_members.items() if member.id in m
    ]


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)


@user.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="who-is",
    description="Displays info about a user",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def user(ctx: lightbulb.Context, member: hikari.Member) -> None:
    target = ctx.get_guild().get_member(member or ctx.user)

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

    status_emoji = "<:offline:993690653240332318>"
    if target.get_presence():
        if target.get_presence().visible_status == "online":
            status_emoji = "<:online:993689284513112094>"
        elif target.get_presence().visible_status.lower() == "idle":
            status_emoji = "<:idle:993689681134882957>"
        elif target.get_presence().visible_status.lower() == "dnd":
            status_emoji = "<:dnd:993690209575248004>"

    type_ = "N/A"
    name = ""

    if target.get_presence() and target.get_presence().activities:
        a = target.get_presence().activities[0]
        type_ = a.type.name.lower().replace("custom", "").title()
        name = a.name

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
            f"{type_} {name}",
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
    await ctx.respond(embed=embed)


@user.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="banner",
    description="Displays the member's banner",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def banner(ctx: lightbulb.Context, member: hikari.Member) -> None:
    target = ctx.get_guild().get_member(member or ctx.user)

    member = target
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    banner = target.banner_url
    if banner:
        embed = hikari.Embed(
            title="Banner Viewer",
            description=f"{target.mention}'s Banner",
            color=color,
            timestamp=datetime.now().astimezone(),
        )
        embed.set_image(banner)
        await ctx.respond(embed=embed)
    else:
        await ctx.respond("The user you specified doesn't have a banner set.")


@user.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="avatar",
    description="Displays the avatar of a Discord member or yours",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar(ctx: lightbulb.Context, member: hikari.Member) -> None:
    target = ctx.get_guild().get_member(member or ctx.user)

    member = target
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    embed = hikari.Embed(
        description=f"{target.mention}'s Avatar",
        color=color,
        timestamp=datetime.now().astimezone(),
    )
    embed.set_image(target.avatar_url or target.default_avatar_url)
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(user)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(user)
