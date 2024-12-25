from __future__ import annotations

import math
from collections import Counter
from datetime import datetime

import hikari
import lightbulb

from bobert.core.utils import constants as const
from bobert.core.utils import format_dt

server = lightbulb.Plugin("server")
server.add_checks(lightbulb.checks.guild_only)


def get_everyone_role(guild):
    for role in guild.get_roles().values():
        if role.position == 0:
            return role


@server.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="server-info",
    description="Displays server information",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def server_cmd(ctx: lightbulb.SlashContext) -> None:
    guild = ctx.get_guild()

    if guild is None:
        await ctx.respond(
            "❌ Unable to fetch guild information.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    ms = guild.get_members()
    cs = guild.get_channels()
    owner = await guild.fetch_owner()

    count_static = len(
        [emoji for emoji in guild.get_emojis().values() if not emoji.is_animated]
    )
    count_animated = len(
        [emoji for emoji in guild.get_emojis().values() if emoji.is_animated]
    )
    emoji_slots = int(
        (
            (1 + (sqrt_5 := math.sqrt(5))) ** (n := guild.premium_tier + 2)
            - (1 - sqrt_5) ** n
        )
        / (2**n * sqrt_5)
        * 50
    )
    total_emoji = int(
        (
            (1 + (sqrt_5 := math.sqrt(5))) ** (n := guild.premium_tier + 2)
            - (1 - sqrt_5) ** n
        )
        / (2**n * sqrt_5)
        * 50
        * 2
    )

    count_text = len(
        [c for c in cs.values() if c.type == hikari.ChannelType.GUILD_TEXT]
    )
    count_voice = len(
        [c for c in cs.values() if c.type == hikari.ChannelType.GUILD_VOICE]
    )
    count_forum = len(
        [c for c in cs.values() if c.type == hikari.ChannelType.GUILD_FORUM]
    )
    count_stage = len(
        [c for c in cs.values() if c.type == hikari.ChannelType.GUILD_STAGE]
    )

    p_view = ctx.bot.cache.get_presences_view_for_guild(guild.id)
    online_members = [m for m in p_view.values() if m.visible_status == "online"]
    idle = [m for m in p_view.values() if m.visible_status == "idle"]
    dnd = [m for m in p_view.values() if m.visible_status == "dnd"]
    ls = []
    ls.extend(online_members)
    ls.extend(idle)
    ls.extend(dnd)
    offline_invisible = len(guild.get_members()) - len(ls)

    everyone = get_everyone_role(guild)

    if everyone is None:
        await ctx.respond(
            "❌ Unable to fetch the everyone role.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    # Get everyone permissions
    everyone_perms = everyone.permissions

    all_text = len(
        [
            c
            for c in guild.get_channels().values()
            if isinstance(c, hikari.GuildTextChannel)
        ]
    )
    all_voice = len(
        [
            c
            for c in guild.get_channels().values()
            if isinstance(c, hikari.GuildVoiceChannel)
        ]
    )
    all_forum = len(
        [
            c
            for c in guild.get_channels().values()
            if isinstance(c, hikari.GuildForumChannel)
        ]
    )
    all_stage = len(
        [
            c
            for c in guild.get_channels().values()
            if isinstance(c, hikari.GuildStageChannel)
        ]
    )

    hidden_voice = 0
    hidden_text = 0
    hidden_forum = 0
    hidden_stage = 0
    all_channels = 0

    for channel in cs.values():
        if ctx.guild_id is None:
            continue

        overwrites = channel.permission_overwrites.get(ctx.guild_id)
        perms = everyone_perms
        if overwrites:
            perms |= overwrites.allow
            perms &= ~overwrites.deny

        all_channels += 1
        if (
            isinstance(channel, hikari.GuildTextChannel)
            and hikari.Permissions.VIEW_CHANNEL not in perms
        ):
            hidden_text += 1
        elif (
            isinstance(channel, hikari.GuildVoiceChannel)
            and hikari.Permissions.CONNECT not in perms
        ):
            hidden_voice += 1
        elif (
            isinstance(channel, hikari.GuildForumChannel)
            and hikari.Permissions.VIEW_CHANNEL not in perms
        ):
            hidden_forum += 1
        elif (
            isinstance(channel, hikari.GuildStageChannel)
            and hikari.Permissions.CONNECT not in perms
        ):
            hidden_stage += 1

    embed = (
        hikari.Embed(
            title=f"{guild.name}",
            description=f"""**ID:** {guild.id}
**Owner:** {owner}
**Description:** {guild.description}""",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Features",
            f"""{f"{const.EMOJI_POSITIVE}" if "COMMUNITY" in guild.features else f"{const.EMOJI_NEGATIVE}"} : Community
{f"{const.EMOJI_POSITIVE}" if "BANNER" in guild.features else f"{const.EMOJI_NEGATIVE}"} : Banner
{f"{const.EMOJI_POSITIVE}" if "GUILD_SERVER_GUIDE" in guild.features else f"{const.EMOJI_NEGATIVE}"} : Server Guide
{f"{const.EMOJI_POSITIVE}" if "NEWS" in guild.features else f"{const.EMOJI_NEGATIVE}"} : News Channel""",
            inline=True,
        )
        .add_field(
            "Channels",
            f"""{const.EMOJI_TEXT} {all_text} ({hidden_text} locked)
{const.EMOJI_VOICE} {all_voice} ({hidden_voice} locked)
{const.EMOJI_FORUM} {all_forum} ({hidden_forum} locked)
{const.EMOJI_STAGE} {all_stage} ({hidden_stage} locked)""",
            inline=True,
        )
        .add_field(
            "Population",
            f"""Total: {len(ms)} ({len([m for m in ms.values() if not m.is_bot])} humans and {len([m for m in ms.values() if m.is_bot])} bots)
{const.EMOJI_ONLINE} : {len(online_members)}  {const.EMOJI_IDLE} : {len(idle)}  {const.EMOJI_DND} : {len(dnd)}  {const.EMOJI_OFFLINE} : {offline_invisible}""",
            inline=False,
        )
        .add_field(
            "Roles",
            f"{len(guild.get_roles())} roles",
            inline=False,
        )
        .add_field(
            "Perferred Locale",
            f"{guild.preferred_locale}",
            inline=False,
        )
        .add_field(
            "Creation Date",
            f"{format_dt(guild.created_at)} ({format_dt(guild.created_at, style='R')})",
            inline=False,
        )
        .add_field(
            "Emoji",
            f"""Static: {count_static}/{emoji_slots}
Animated: {count_animated}/{emoji_slots}
Total: {len(guild.get_emojis())}/{total_emoji}""",
            inline=True,
        )
        .add_field(
            "Boost Status",
            f"""Total: {guild.premium_subscription_count}
Tier: {(guild.premium_tier) if guild.premium_tier else "0"}""".replace(
                "TIER_", ""
            ),
            inline=True,
        )
        .set_thumbnail(guild.icon_url)
        .set_footer(text=f"Requested by {ctx.user}")
    )
    await ctx.respond(embed=embed)


@server.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="server-icon",
    description="Displays the servers' icon",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def server_icon_cmd(ctx: lightbulb.SlashContext) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "❌ The guild ID is missing. Cannot fetch guild information.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    guild = ctx.bot.cache.get_guild(ctx.guild_id) or await ctx.bot.rest.fetch_guild(
        ctx.guild_id
    )

    embed = hikari.Embed(
        title=f"{guild.name}'s server icon:",
    )
    embed.set_image(guild.icon_url)
    await ctx.respond(embed=embed)


@server.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to get the information from",
    type=hikari.Role,
    required=True,
)
@lightbulb.command(
    name="role-info",
    description="Displays information about a role",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def role_info_cmd(ctx: lightbulb.SlashContext, role: hikari.Role) -> None:
    """Allows mentioning of a role or to use the ID of one when using the role option."""
    guild = ctx.get_guild()

    if guild is None:
        await ctx.respond(
            "❌ Unable to retrieve guild information.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    ms = guild.get_members()

    embed = (
        hikari.Embed(
            title=f"`{role.name}`",
            color=role.color or None,
            description=f"**ID**: `{role.id}`",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Administrator?",
            f"{bool(role.permissions & hikari.Permissions.ADMINISTRATOR)}",
            inline=True,
        )
        .add_field(
            "Mentionable?",
            f"{role.is_mentionable}",
            inline=True,
        )
        .add_field(
            "Color",
            f"{role.color.hex_code}",
            inline=True,
        )
        .add_field(
            "Role Position",
            f"{role.position}",
            inline=True,
        )
        .add_field(
            "Members",
            f"{len([m for m in  ms.values() if role.id in m.role_ids])}",
            inline=True,
        )
        .add_field(
            "Creation Date",
            f"{format_dt(role.created_at)} ({format_dt(role.created_at, style='R')})",
            inline=False,
        )
        .set_footer(
            text=f"Requested by {ctx.member.username if ctx.member else 'Unknown'}",
            icon=(
                ctx.member.avatar_url
                if ctx.member and ctx.member.avatar_url
                else ctx.member.default_avatar_url if ctx.member else None
            ),
        )
    )
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(server)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(server)
