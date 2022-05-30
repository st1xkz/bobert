from __future__ import annotations

import math
from collections import Counter
from datetime import datetime

import hikari
import lightbulb

from bobert.core.utils import format_dt

server_plugin = lightbulb.Plugin("server")


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="serverinfo",
    aliases=["server", "si"],
    description="Displays info about the server",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_server(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
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

    p_view = ctx.bot.cache.get_presences_view_for_guild(guild.id)
    online_members = [m for m in p_view.values() if m.visible_status == "online"]
    idle = [m for m in p_view.values() if m.visible_status == "idle"]
    dnd = [m for m in p_view.values() if m.visible_status == "dnd"]
    ls = []
    ls.extend(online_members)
    ls.extend(idle)
    ls.extend(dnd)
    offline_invisible = len(guild.get_members()) - len(ls)

    """
    everyone = guild.get_role(guild.id)
    everyone_perms = everyone.permissions.value
    secret = Counter()
    totals = Counter()
    for channel in guild.get_channels().values():
        allow, deny = channel.permission_overwrites(everyone).pair()
        perms = hikari.Permissions((everyone_perms & -deny.value) | allow.value)
        channel_type = type(channel)
        totals[channel_type] += 1
        if not perms & hikari.Permissions.VIEW_CHANNELS:
            secret[channel_type] += 1
        elif isinstance(channel, hikari.VoiceChannel) and (not perms.CONNECT or not perms.SPEAK):
            secret[channel_type] += 1
    """

    embed = (
        hikari.Embed(
            title=f"{guild.name}",
            description=f"""**ID**: {guild.id}
**Owner**: {owner.username}#{owner.discriminator}
**Description**: {guild.description}""",
            color=0x2F3136,
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Features",
            f"""{"<:yes:979187100907864104>" if "COMMUNITY" in guild.features else "<:no:979185688933199892>"} : Community
{"<:yes:979187100907864104>" if "BANNER" in guild.features else "<:no:979185688933199892>"} : Banner
{"<:yes:979187100907864104>" if "WELCOME_SCREEN_ENABLED" in guild.features else "<:no:979185688933199892>"} : Welcome Screen
{"<:yes:979187100907864104>" if "NEWS" in guild.features else "<:no:979185688933199892>"} : News Channel""",
            inline=True,
        )
        .add_field(
            "Channels",
            f"""<:text:968015733026091038> {count_text} ()
<:voice:968015770527354930> {count_voice}""",
            inline=True,
        )
        .add_field(
            "Population",
            f"""Total: {len(ms)} ({len([m for m in ms.values() if not m.is_bot])} humans and {len([m for m in ms.values() if m.is_bot])} bots)
<:online:968018354910679050> : {len(online_members)}  <:idle:968020508387999834> : {len(idle)}  <:dnd:968020978665943060> : {len(dnd)}  <:offline:968021408116539432> : {offline_invisible}""",
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
Tier: {(guild.premium_tier) if guild.premium_tier else "0"}""",
            inline=True,
        )
        .set_thumbnail(guild.icon_url)
        .set_footer(text=f"Requested by {ctx.user}")
    )
    await ctx.respond(embed)


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="servericon",
    aliases=["sicon"],
    description="Displays the servers icon",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_servericon(ctx: lightbulb.Context) -> None:
    guild = ctx.bot.cache.get_guild(ctx.guild_id) or await ctx.bot.rest.fetch_guild(
        ctx.guild_id
    )
    embed = hikari.Embed(
        title=f"Server Icon for {guild.name}",
        timestamp=datetime.now().astimezone(),
    )
    embed.set_image(guild.icon_url)
    await ctx.respond(embed)


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to get info from",
    type=hikari.Emoji,
    required=True,
)
@lightbulb.command(
    name="emojiinfo",
    aliases=["ei", "emoji", "einfo"],
    description="Displays info about an emoji",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_emoji(ctx: lightbulb.Context) -> None:
    emoji = ctx.get_guild().get_emoji(ctx.options.emoji)

    if not emoji:
        await ctx.respond(
            "The emoji you specified isn't in the server.",
            delete_after=10,
        )
        return

    embed = (
        hikari.Embed(
            title=f"`{emoji.name}`",
            color=0x2F3136,
            description=f"**ID**: `{emoji.id}`",
            timestamp=datetime.utcnow().astimezone(),
        )
        .add_field(
            "Animated?",
            f"{emoji.is_animated}",
            inline=False,
        )
        .add_field(
            "Managed?",
            f"{emoji.is_managed}",
            inline=False,
        )
        .add_field(
            "Available?",
            f"{emoji.is_available}",
            inline=False,
        )
        .add_field(
            "Creation Date",
            f"{format_dt(emoji.created_at)} ({format_dt(emoji.created_at, style='R')})",
            inline=False,
        )
        .add_field(
            "Emoji Creator",
            f"{emoji.user}",
            inline=False,
        )
        .set_thumbnail(emoji.url)
        .set_footer(text=f"Requested by {ctx.user}")
    )
    await ctx.respond(embed=embed)


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to get the information from",
    type=hikari.Role,
    required=True,
)
@lightbulb.command(
    name="roleinfo",
    aliases=["role", "ri"],
    description="Displays info about a role",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_role(ctx: lightbulb.Context) -> None:
    role = ctx.options.role
    ms = ctx.get_guild().get_members()

    embed = (
        hikari.Embed(
            title=f"`{role.name}`",
            color=role.color,
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
            text=f"Requested by {ctx.member.username}#{ctx.member.discriminator}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(server_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(server_plugin)
