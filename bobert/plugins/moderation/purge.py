import datetime

import hikari
import lightbulb

purge_plugin = lightbulb.Plugin("purge")
purge_plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)


@purge_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    "count", "the amount of messages to purge", type=int, max_value=100, min_value=1
)
# You may also use pass_options to pass the options directly to the function
@lightbulb.command(
    "purge", "Purge a certain amount of messages from a channel.", pass_options=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_purge(ctx: lightbulb.SlashContext, count: int) -> None:
    """Purge a certain amount of messages from a channel."""
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    # Fetch messages that are not older than 14 days in the channel the command is invoked in
    # Messages older than 14 days cannot be deleted by bots, so this is a necessary precaution
    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(
            lambda m: datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(days=14)
            > m.created_at
        )
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)
