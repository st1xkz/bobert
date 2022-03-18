import hikari
import lightbulb

import bobert
from bobert.core.utils import chron

import time
import datetime as dt
from datetime import datetime, timedelta
import inspect
import platform
import textwrap
from psutil import Process, virtual_memory
from io import BytesIO


info_plugin = lightbulb.Plugin("info")


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="github", aliases=["git"], description="Gets the link to the bot's GitHub (you may not copy the bot's code and add it to your own)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def git_command(ctx: lightbulb.Context) -> None:
    with open("./LICENSE") as f:
        license_ = f.readline().strip()
    await ctx.respond(
        f"<:githubwhite:935336990482772020> This bot is licensed under the **{license_}**\n"
        "https://github.com/st1xkz/bobert"
    )


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("command", "The command to get the source for")
@lightbulb.command(name="source", aliases=["find", "sc"], description="Gets source code of any command in the bot (you may not copy the bot's code and add it to your own)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_source(ctx: lightbulb.Context) -> None:
    command = ctx.bot.get_slash_command(ctx.options.command)
    
    if command is None:
        await ctx.respond(
            "That command doesn't exist.",
            delete_after=10
        )
    
    code = textwrap.dedent((inspect.getsource(command.callback)))
    m = await ctx.respond(
        f"The source code for command `{command.name}`"
    )
    b = BytesIO(code.encode())
    b.seek(0)
    await m.edit(attachment=hikari.Bytes(b, f"source_{command.name}.py"))


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User, required=False)
@lightbulb.command(name="userinfo", aliases=["user", "whois", "ui"], description="Displays info about a user")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo_command(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10
        )
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())
    target_status = (
        target.get_presence().visible_status if target.get_presence() else "Offline"
    )

    roles = (await target.fetch_roles())[1:]

    embed = (
        hikari.Embed(
            title=f"User Info - {target.username}#{target.discriminator}",
            description=f"ID: `{target.id}`",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Nickname",
            f"{target.nickname}",
            inline=True,
        )
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Status",
            f"{target_status.title()}",
            inline=True,
        )
        .add_field(
            "Boosted?",
            f"{target.premium_since}",
            inline=True,
        )
        .add_field(
            "Account Created",
            f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=False,
        )
        .add_field(
            "Joined",
            f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline=False,
        )
        .add_field(
            f"Roles [{len(roles)}]",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
        .set_thumbnail(
            target.avatar_url or target.default_avatar_url,
        )
        .set_footer(
            text=f"Requested by {ctx.member.username}#{ctx.member.discriminator}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url
        )
    )
    await ctx.respond(embed)


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="serverinfo", aliases=["server", "si"], description="Displays info about the server")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_guild_info(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    ms = guild.get_members()
    cs = guild.get_channels()
    owner = await guild.fetch_owner()
    list_of_bots = [m.mention for m in ms.values() if m.is_bot]

    embed = (
        hikari.Embed(
            title=f"Server Info - {guild.name}",
            description=f"{guild.description}",
            color=0x2f3136,
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Owner",
            f"{owner.mention}",
            inline=True,
        )
        .add_field(
            "Emoji Count",
            f"{len(guild.get_emojis())}",
            inline=True,
        )
        .add_field(
            "Role Count",
            f"{len(guild.get_roles())}",
            inline=True,
        )
        .add_field(
            "Humans",
            f"{len([m for m in ms.values() if not m.is_bot])}",
            inline=True,
        )
        .add_field(
            "Population",
            f"{len(ms)}",
            inline=True,
        )
        .add_field(
            "Text",
            f"{len([c for c in cs.values() if c.type == hikari.ChannelType.GUILD_TEXT])}",
            inline=True,
        )
        .add_field(
            "Voice",
            f"{len([c for c in cs.values() if c.type == hikari.ChannelType.GUILD_VOICE])}",
            inline=True,
        )
        .add_field(
            f"Bots [{len([m for m in ms.values() if m.is_bot])}]",
            f', '.join(list_of_bots),
            inline=False,
        )
        .add_field(
            "Creation Date",
            f"<t:{int(guild.created_at.timestamp())}:f>",
            inline=False,
        )
        .add_field(
            "Verification Level",
            f"{guild.verification_level.name.title()}",
            inline=True,
        )
        .add_field(
            "Default Message Notifications",
            f"{guild.default_message_notifications.name.title()}",
            inline=True,
        )
        .add_field(
            "Explicit Content Filter",
            str(guild.explicit_content_filter).lower(),
            inline=True,
        )
        .add_field(
            "Total Boosts",
            f"{guild.premium_subscription_count}",
            inline=True,
        )
        .add_field(
            "Boost Tier",
            f"{(guild.premium_tier) if guild.premium_tier else '0'}",
            inline=True,
        )
        .set_thumbnail(
            guild.icon_url
        )
        .set_footer(
            text=f"Guild ID: {guild.id}",
            icon=guild.icon_url
        )
    )
    await ctx.respond(embed)


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("role", "The role to get the information from", hikari.Role)
@lightbulb.command(name="roleinfo", aliases=["role", "ri"], description="Displays info about a role")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def roleinfo_command(ctx: lightbulb.Context) -> None:
    role = ctx.options.role
    ms = ctx.get_guild().get_members()

    role_created = int(role.created_at.timestamp())

    embed = (
        hikari.Embed(
            title=f"Role Info - {role.name}",
            color=role.color,
            description=f"ID: `{role.id}`",
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
            "Created At",
            f"<t:{role_created}:f> (<t:{role_created}:R>)",
            inline=False,
        )
        .set_footer(
            text=f"Requested by {ctx.member.username}#{ctx.member.discriminator}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
    )
    await ctx.respond(embed)


@info_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="botinfo", aliases=["bot", "stats"], description="Displays info about the bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_bot_info(ctx: lightbulb.Context) -> None:
    if not (guild := ctx.get_guild()):
        return

    if not (me := guild.get_my_member()):
        return

    if not (member := ctx.member):
        return

    with (proc := Process()).oneshot():
        uptime = chron.short_delta(
            dt.timedelta(seconds=time.time() - proc.create_time())
        )
        cpu_time = chron.short_delta(
            dt.timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user),
            ms=True,
        )
        mem_total = virtual_memory().total / (1024 ** 2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
        bot_user = ctx.bot.get_me()

        embed = (
            hikari.Embed(
                title="Statistics for Bobert",
                description=f"Guild Count: **{len(ctx.bot.cache.get_available_guilds_view())}**\nUser Count: **{len(ctx.bot.cache.get_users_view())}**\nCommand Count: **{len(ctx.bot.slash_commands)}**\n\nUptime: **{uptime}**\nCPU Time: **{cpu_time}**\nMemory Usage: **{mem_usage:,.3f}/{mem_total:,.0f} MiB ({mem_of_total:,.0f}%)**\n\nLanguage: **Python**\nPython Version: **v{platform.python_version()}**\nLibrary: **hikari-py v{hikari.__version__}**\nCommand Handler: **hikari-lightbulb v{lightbulb.__version__}**",
                timestamp=datetime.now().astimezone(),
            )
            .set_thumbnail(
                bot_user.avatar_url or bot_user.default_avatar_url,
            )
            .set_footer(
                text=f"Bot developed by sticks#5822"
            )
        )
        await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(image_plugin)