import hikari
import lightbulb


confess_plugin = lightbulb.Plugin("confess")


"""
@confess_plugin.command
@lightbulb.command(
    name="confess",
    description="Sends user's confession to the <#806649874379964487> channel through DMs",
    auto_defer=True,
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ass_command(ctx: lightbulb.Context) -> None:
    pass
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess_plugin)