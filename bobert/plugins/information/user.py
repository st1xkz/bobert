import hikari
import lightbulb

from bobert.core.utils import format_dt
from bobert.core.stuff.badges import *

from datetime import datetime
from typing import Sequence


user_plugin = lightbulb.Plugin("user")


def sort_roles(roles: Sequence[hikari.Role]) -> Sequence[hikari.Role]:
    return sorted(roles, key=lambda r: r.position, reverse=True)


@user_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="userinfo",
    aliases=["user", "whois", "ui"],
    description="Displays info about a user",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_user(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    roles = [role.mention for role in sort_roles(target.get_roles())]
    roles.remove(f"<@&{ctx.guild_id}>")
    roles = ", ".join(roles) if roles else "No roles"
    role_num = (await target.fetch_roles())[1:]

    guild = ctx.get_guild()
    member_count = len([m for m in guild.get_members().values() if m.joined_at < target.joined_at])+1
    
    status_emoji = "<:offline:968021408116539432>"
    if target.get_presence():
        if target.get_presence().visible_status == "online":
            status_emoji = "<:online:968018354910679050>"
        elif target.get_presence().visible_status.lower() == "idle":
            status_emoji = "<:idle:968020508387999834>"
        elif target.get_presence().visible_status.lower() == "dnd":
            status_emoji = "<:dnd:968020978665943060>"
    
    type_ = "N/A"
    name = ""

    if target.get_presence() and target.get_presence().activities:
        a = target.get_presence().activities[0]
        type_ = a.type.name.lower().replace("custom", "").title()
        name = a.name

    embed = (
        hikari.Embed(
            title=f"{status_emoji} {target.username}#{target.discriminator} ~ {target.nickname}" if target.nickname else f"{status_emoji} {target.username}",
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
    await ctx.respond(embed)


@user_plugin.command
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
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_banner(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    banner = target.banner_url
    if banner:
        embed = (
            hikari.Embed(
                title="Banner Viewer",
                description=f"{target.mention}'s Banner",
                timestamp=datetime.now().astimezone(),
            )
            .set_image(
                banner
            )
        )
        await ctx.respond(embed)
    else:
        await ctx.respond(
            "The user you specified doesn't have a banner set."
        )


@user_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="avatar",
    aliases=["ava"],
    description="Displays the avatar of a Discord member or yours",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_avatar(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    avatar = target.avatar_url or target.default_avatar_url
    if avatar:
        embed = (
            hikari.Embed(
                description=f"{target.mention}'s Avatar",
                timestamp=datetime.now().astimezone(),
            )
            .set_image(
                target.avatar_url or target.default_avatar_url
            )
        )
        await ctx.respond(embed)
    else:
        await ctx.respond(
            "The user you specified doesn't have an avatar set."
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(user_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(user_plugin)