import asyncio

import hikari
import lightbulb
from lightbulb import errors

purge_plugin = lightbulb.Plugin("purge")


@purge_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
)
@lightbulb.option(
    name="messages",
    description="the number of messages to delete",
    type=int,
    required=True,
)
@lightbulb.command(
    name="purge",
    aliases=["clear"],
    description="Deletes optional number of messages",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_purge(ctx: lightbulb.Context) -> None:
    num_msgs = ctx.options.messages
    channel = ctx.channel_id

    if isinstance(ctx, lightbulb.PrefixContext):
        await ctx.event.message.delete()

    msgs = await ctx.bot.rest.fetch_messages(channel).limit(num_msgs)
    await ctx.bot.rest.delete_messages(channel, msgs)

    await ctx.respond(f"**{len(msgs)}** messages were deleted", delete_after=5)

    await asyncio.sleep(5)


@cmd_purge.set_error_handler
async def on_purge_error(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    if isinstance(exc, errors.NotEnoughArguments):
        await ctx.respond(
            "You must specify the number of messages to delete.", delete_after=10
        )
        return True

    return False


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)
