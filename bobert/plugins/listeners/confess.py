import hikari
import lightbulb


confess_plugin = lightbulb.Plugin("confess")


@confess_plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent) -> None:
    message = event.content
    if message.author.is_bot:
        return
    if message.channel.id == 900458968588120154:
        pass


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess_plugin)