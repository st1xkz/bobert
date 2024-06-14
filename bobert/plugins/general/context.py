from __future__ import annotations

import typing
from datetime import datetime
from typing import Sequence

import hikari
import lightbulb
import miru

from bobert.core.stuff.badges import *
from bobert.core.utils import constants as const
from bobert.core.utils import format_dt, helpers

context = lightbulb.Plugin("context")


def mutual_guilds(bot: hikari.GatewayBot, member: hikari.Member) -> list[hikari.Guild]:
    all_members = bot.cache.get_members_view()
    return [
        bot.cache.get_guild(guild) for guild, m in all_members.items() if member.id in m
    ]


def get_status(activity: typing.Optional[hikari.Activity]) -> str:
    if activity is None:
        return "No Activity"

    type_ = activity.type
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
async def show_user(ctx: lightbulb.UserContext) -> None:
    target = ctx.bot.cache.get_member(ctx.guild_id, ctx.options.target.id)

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

    roles = [
        role.mention
        for role in helpers.sort_roles(target.get_roles())
        if role.id != ctx.guild_id
    ]
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

    if target.get_presence() is None:
        activity = "No Activity"
    else:
        activity = ac[0] if (ac := target.get_presence().activities) else None

    embed = (
        hikari.Embed(
            title=(
                f"{status_emoji} {target.username}#{target.discriminator} ~ {target.nickname}"
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
async def show_avatar(ctx: lightbulb.UserContext) -> None:
    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)

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


# FIXME: Add duration to mute command
class MuteReason(miru.Modal, title="Mute Member"):
    reason = miru.TextInput(
        label="Reason",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Provide the reason for the mute",
        max_length=500,
    )

    def __init__(self, target: hikari.Member, role: hikari.Role):
        super().__init__()
        self.target = target
        self.role = role

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()

        await self.target.add_role(self.role.id)
        await ctx.respond(
            f"You have muted {self.target.mention}.", flags=hikari.MessageFlag.EPHEMERAL
        )

        # Send to mod-logs
        embed = hikari.Embed(
            title="Member Updated",
            description=f"{const.EMOJI_MUTE} A member {self.target.mention} has been muted",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Reason:",
            value=self.reason.value,
        )
        embed.set_author(
            name=f"Muted by {ctx.author} ({ctx.author.id})",
            icon=ctx.author.display_avatar_url,
        )
        embed.set_footer(text=f"UID: {self.target.id}")
        await context.bot.rest.create_message(825402276721721355, embed=embed)


@context.command
@lightbulb.command(name="Mute", description="Mutes the user")
@lightbulb.implements(lightbulb.UserCommand)
async def mute_user(ctx: lightbulb.UserContext) -> None:
    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
    role = next(
        (role for role in ctx.get_guild().get_roles().values() if role.name == "Muted"),
        None,
    )

    if target is None:
        await ctx.respond(
            "User not found or not in this server.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    if role is None:
        await ctx.respond(
            "Role not found or invalid role specified.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if role.id in target.role_ids:
        await ctx.respond(
            "This user is already muted.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    modal = MuteReason(target, role)
    builder = modal.build_response(ctx.bot.d.miru)
    await builder.create_modal_response(ctx.interaction)
    ctx.bot.d.miru.start_modal(modal)


@context.command
@lightbulb.command(name="Remove Mute", description="Removes the mute")
@lightbulb.implements(lightbulb.UserCommand)
async def unmute_user(ctx: lightbulb.UserContext) -> None:
    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
    role = next(
        (role for role in ctx.get_guild().get_roles().values() if role.name == "Muted"),
        None,
    )

    await target.remove_role(role.id)
    if role.id not in target.role_ids:
        await ctx.respond(
            "This user is not currently muted.", flags=hikari.MessageFlag.EPHEMERAL
        )
    else:
        await ctx.respond(
            f"You have unmuted {target.mention}.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        # Send to mod-logs
        embed = hikari.Embed(
            title="Member Mute Removed",
            description=f"{const.EMOJI_MUTE} A member {target.mention} has had their mute removed",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.set_author(
            name=f"Removed by {ctx.author} ({ctx.author.id})",
            icon=ctx.author.display_avatar_url,
        )
        embed.set_footer(text=f"UID: {target.id}")
        await context.bot.rest.create_message(825402276721721355, embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(context)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(context)
