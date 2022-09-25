import hikari
import lightbulb

lock_plugin = lightbulb.Plugin("lock")
lock_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS)
)


@lock_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for lockdown",
    required=False,
)
@lightbulb.command(
    name="serverlock",
    description="Locks the entire server",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_server_lock(ctx: lightbulb.Context) -> None:
    channels = await ctx.bot.rest.fetch_guild_channels(ctx.guild_id)

    for channel in channels:
        if not isinstance(channel, hikari.GuildTextChannel):
            continue

        await channel.edit_overwrite(
            ctx.guild_id,
            target_type=hikari.PermissionOverwriteType.ROLE,
            deny=hikari.Permissions.SEND_MESSAGES,
            reason="Server lockdown",
        )
    await ctx.respond(
        f"⚠️ Server has been put in lockdown by `{ctx.user}`.\n"
        f"**Reason**: {ctx.options.reason or 'None'}"
    )


@lock_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for unlocking the server",
    required=False,
)
@lightbulb.command(
    name="serverunlock",
    description="Unlocks the entire server",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_server_unlock(ctx: lightbulb.Context) -> None:
    channels = await ctx.bot.rest.fetch_guild_channels(ctx.guild_id)

    for channel in channels:
        if not isinstance(channel, hikari.GuildTextChannel):
            continue

        await channel.edit_overwrite(
            ctx.guild_id,
            target_type=hikari.PermissionOverwriteType.ROLE,
            deny=hikari.Permissions.NONE,
            reason="Server unlock",
        )
    await ctx.respond(
        f"⚠️ Server has been unlocked by `{ctx.user}`.\n"
        f"**Reason**: {ctx.options.reason or 'None'}"
    )


@lock_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for channel lockdown",
    required=False,
)
@lightbulb.option(
    name="channel",
    description="the channel to lock",
    type=hikari.TextableGuildChannel,
    required=False,
)
@lightbulb.command(
    name="lock",
    description="Locks a channel",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_lock(ctx: lightbulb.Context) -> None:
    channel = ctx.options.channel or ctx.get_channel()

    await channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.SEND_MESSAGES,
        reason="Channel lockdown",
    )

    await ctx.respond(
        f"⚠️ {channel.mention} has been locked by `{ctx.user}`.\n"
        f"**Reason**: {ctx.options.reason or 'None'}"
    )


@lock_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning to unlock a channel",
    required=False,
)
@lightbulb.option(
    name="channel",
    description="the channel to unlock",
    type=hikari.TextableGuildChannel,
    required=False,
)
@lightbulb.command(
    name="unlock",
    description="Unlocks a channel",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_unlock(ctx: lightbulb.Context) -> None:
    channel = ctx.options.channel or ctx.get_channel()

    await channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.NONE,
        reason="Channel unlock",
    )

    await ctx.respond(
        f"⚠️ {channel.mention} has been unlocked by `{ctx.user}`.\n"
        f"**Reason**: {ctx.options.reason or 'None'}"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lock_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(lock_plugin)
