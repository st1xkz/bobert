import datetime

import hikari
import lightbulb

purge_plugin = lightbulb.Plugin("purge")
purge_plugin.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES)
)


@purge_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="amount",
    description="the number of messages to delete",
    type=int,
    max_value=100,
    min_value=1,
    required=True,
)
@lightbulb.command(
    name="purge",
    description="Deletes optional number of messages",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_purge(ctx: lightbulb.Context) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

        # fetch messages that are not older than 14 days in the channel the command was invoked in
        # messages older than 14 days be deleted by bots, so it's unnecessary
        messages = (
            await ctx.bot.rest.fetch_messages(ctx.guild_id)
            .take_until(
                lambda m: datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=14)
                > m.created_at
            )
            .limit(ctx.options.amount)
        )

        if messages:
            await ctx.bot.rest.delete_messages(ctx.channel_id, messages)
            await ctx.respond(
                f"<:yes:993687377841234022> Purged {len(ctx.options.amount)} messages"
            )
        else:
            await ctx.respond(
                "<:no:993686064805978182> Couldn't find any messages younger than 14 days!"
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge_plugin)
