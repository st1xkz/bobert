import hikari
import lightbulb

ticket_plugin = lightbulb.Plugin("ticket")


@lock_plugin.command
@lightbulb.command(name="foo", description="bar")
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd(ctx: lightbulb.Context) -> None:
    await ctx.respond("hikari")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket_plugin)
