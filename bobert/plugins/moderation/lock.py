import hikari
import lightbulb

lock = lightbulb.Plugin("lock")
lock.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS)
)

# FIXME: find out why message won't send to the channel but still works fine
@lock.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for lockdown",
    required=False,
)
@lightbulb.command(
    name="server-lock",
    description="Locks the entire server",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def server_lock(ctx: lightbulb.Context, reason: str) -> None:
    """If `reason` is not specified, it will be set to None"""
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
        f"⚠️ Server has been put on lockdown by **{ctx.user}**.\n"
        f"**Reason**: {reason or 'None'}"
    )


@lock.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for unlocking the server",
    required=False,
)
@lightbulb.command(
    name="server-unlock",
    description="Unlocks the entire server",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def server_unlock(ctx: lightbulb.Context, reason: str) -> None:
    """If `reason` is not specified, it will be set to None"""
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
        f"⚠️ Server has been unlocked by **{ctx.user}**.\n"
        f"**Reason**: {reason or 'None'}"
    )


# FIXME: fix error: AtrributeError: 'InteractionChannel' object has no attribute 'edit_overwrite'
@lock.command
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
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _lock(
    ctx: lightbulb.Context, channel: hikari.TextableGuildChannel, reason: str
) -> None:
    """
    Allows mentioning of a channel or to use the id of one when using the channel option. If `reason` is not specified, it will be set to None
    """
    _channel = channel or ctx.get_channel()

    await _channel.edit_permission_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.SEND_MESSAGES,
        reason="Channel lockdown",
    )

    await ctx.respond(
        f"⚠️ {_channel.mention} has been locked by **{ctx.user}**.\n"
        f"**Reason**: {reason or 'None'}"
    )


# FIXME: fix error: AtrributeError: 'InteractionChannel' object has no attribute 'edit_overwrite'
@lock.command
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
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def unlock(
    ctx: lightbulb.Context, channel: hikari.TextableGuildChannel, reason: str
) -> None:
    """
    Allows mentioning of a channel or to use the id of one when using the channel option. If `reason` is not specified, it will be set to None
    """
    _channel = channel or ctx.get_channel()

    await _channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.NONE,
        reason="Channel unlock",
    )

    await ctx.respond(
        f"⚠️ {_channel.mention} has been unlocked by **{ctx.user}**.\n"
        f"**Reason**: {reason or 'None'}"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lock)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(lock)
