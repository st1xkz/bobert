import hikari
import lightbulb

ticket = lightbulb.Plugin("ticket")


@ticket.command
@lightbulb.command(name="idk", description="this does stuff")
@lightbulb.implements(lightbulb.SlashCommand)
async def this_idk(ctx: lightbulb.Context) -> None:
    ...


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings)
