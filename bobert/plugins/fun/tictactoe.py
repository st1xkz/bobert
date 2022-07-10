import hikari
import lightbulb
import random


tictactoe_plugin = lightbulb.Plugin("tic-tac-toe")


@tictactoe_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="player",
    description="the user to play Tic-Tac-Toe with",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_tictactoe(ctx: lightbulb.Context) -> None:
    pass


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tictactoe_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tictactoe_plugin)