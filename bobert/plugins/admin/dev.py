import os
import sys

import lightbulb

dev = lightbulb.Plugin("dev")
dev.add_checks(lightbulb.checks.owner_only)


@dev.command()
@lightbulb.command(
    name="restart",
    description="Restarts the bot",
    hidden=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def restart(ctx: lightbulb.Context) -> None:
    await ctx.respond("Restarting...")
    await ctx.bot.close()
    os.system("clear")
    os.execv(sys.executable, ["python"] + sys.argv)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dev)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dev)
