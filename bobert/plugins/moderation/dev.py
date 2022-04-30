import lightbulb

import os
import sys


dev_plugin = lightbulb.Plugin("dev")
dev_plugin.add_checks(lightbulb.checks.owner_only)


@dev_plugin.command()
@lightbulb.command(
    name="shutdown",
    aliases=["bye", "fuckoff"],
    description="Shuts the bot down",
    hidden=True,
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        "Shutting down..."
    )
    await ctx.bot.close()
    await sys.exit()


@dev_plugin.command()
@lightbulb.command(
    name="restart",
    aliases=["hi", "wake"],
    description="Restarts the bot",
    hidden=True,
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_restart(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        "Restarting..."
    )
    await ctx.bot.close()
    os.system("clear")
    os.execv(sys.executable, ["python"] + sys.argv)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dev_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dev_plugin)