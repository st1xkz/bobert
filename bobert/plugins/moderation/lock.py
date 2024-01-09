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
    description="the reasoning for locking channel",
    required=False,
)
@lightbulb.option(
    name="channel",
    description="the channel to lock",
    type=hikari.TextableGuildChannel,
    channel_types=[hikari.ChannelType.GUILD_TEXT],
    required=False,
)
@lightbulb.command(
    name="lock",
    description="Lock a channel",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _lock(
    ctx: lightbulb.Context, channel: hikari.TextableGuildChannel, reason: str
) -> None:
    """
    Allows mentioning of a channel or to use the ID of one when using the channel option. If `reason` is not specified, it will be set to None.
    """
    _channel = ctx.get_guild().get_channel(channel.id if channel else ctx.channel_id)

    await _channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.SEND_MESSAGES,
        reason=reason or "Channel lockdown",
    )

    if (
        _channel.permission_overwrites.get(ctx.guild_id).deny
        & hikari.Permissions.SEND_MESSAGES
    ):
        await ctx.respond(
            "❌ This channel has already been locked.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    else:
        await ctx.respond(
            f"⚠️ {_channel.mention} has been locked by **{ctx.user}**.\n"
            f"**Reason**: {reason or 'None'}"
        )


@lock.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning to unlock channel",
    required=False,
)
@lightbulb.option(
    name="channel",
    description="the channel to unlock",
    type=hikari.TextableGuildChannel,
    channel_types=[hikari.ChannelType.GUILD_TEXT],
    required=False,
)
@lightbulb.command(
    name="unlock",
    description="Unlock a previously locked channel",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def unlock(
    ctx: lightbulb.Context, channel: hikari.TextableGuildChannel, reason: str
) -> None:
    """
    Allows mentioning of a channel or to use the ID of one when using the channel option. If `reason` is not specified, it will be set to None.
    """
    _channel = ctx.get_guild().get_channel(channel.id if channel else ctx.channel_id)

    await _channel.edit_overwrite(
        ctx.guild_id,
        target_type=hikari.PermissionOverwriteType.ROLE,
        deny=hikari.Permissions.NONE,
        reason=reason or "Channel unlock",
    )
    if (
        _channel.permission_overwrites.get(ctx.guild_id).unset
        & hikari.Permissions.SEND_MESSAGES
    ):
        await ctx.respond(
            "❌ This channel has already been unlocked.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
    else:
        await ctx.respond(
            f"⚠️ {_channel.mention} has been unlocked by **{ctx.user}**.\n"
            f"**Reason**: {reason or 'None'}"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(lock)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(lock)
