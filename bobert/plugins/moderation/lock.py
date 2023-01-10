import hikari
import lightbulb

lock = lightbulb.Plugin("lock")
lock.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_CHANNELS)
)


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
    Allows mentioning of a channel or to use the id of one when using the channel option. If `reason` is not specified, it will be set to None.
    """
    _channel = ctx.get_guild().get_channel(channel.id if channel else ctx.channel_id)

    await _channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.SEND_MESSAGES,
        reason="Channel lockdown",
    )

    await ctx.respond(
        f"⚠️ {_channel.mention} has been locked by **{ctx.user}**.\n"
        f"**Reason**: {reason or 'None'}"
    )


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
    Allows mentioning of a channel or to use the id of one when using the channel option. If `reason` is not specified, it will be set to None.
    """
    _channel = ctx.get_guild().get_channel(channel.id if channel else ctx.channel_id)

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
