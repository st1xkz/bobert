import hikari
import lightbulb

import asyncio
from lightbulb import errors

plugin = lightbulb.Plugin("mod")

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES),
    lightbulb.bot_has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)
@lightbulb.option("messages", "The number of messages to delete", type=int, required=True)
@lightbulb.command(name="purge", aliases=["clear"], description="Deletes optional number of messages")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def purge_messages(ctx: lightbulb.Context) -> None:
    num_msgs = ctx.options.messages
    channel = ctx.channel_id

    if isinstance(ctx, lightbulb.PrefixContext):
        await ctx.event.message.delete()

    msgs = await ctx.bot.rest.fetch_messages(channel).limit(num_msgs)
    await ctx.bot.rest.delete_messages(channel, msgs)

    resp = await ctx.respond(f"**{len(msgs)}** messages were deleted")

    await asyncio.sleep(5)
    await resp.delete()

@purge_messages.set_error_handler
async def on_purge_error(event: lightbulb.CommandErrorEvent) -> bool:
    exc = event.exception.__cause__ or event.exception
    ctx = event.context

    if isinstance(exc, errors.NotEnoughArguments):
        await ctx.respond(
            "You must specify the number of messages to delete.",
            delete_after=10
        )
        return True
        
    return False


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)