import hikari
import lightbulb

import os
import sys
import random
from bobert.core.stuff import shutdown, restart


tools_plugin = lightbulb.Plugin("tools")
tools_plugin.add_checks(lightbulb.checks.owner_only)


@tools_plugin.command()
@lightbulb.command(
    name="shutdown",
    aliases=["bye", "fuckoff"],
    description="Shuts the bot down",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def shutdown_command(ctx: lightbulb.Context) -> None:
    await ctx.respond(random.choice(shutdown))
    await ctx.bot.close()
    await sys.exit()


@tools_plugin.command()
@lightbulb.command(
    name="restart",
    aliases=["hi", "wake"],
    description="Restarts the bot",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def restart_command(ctx: lightbulb.Context) -> None:
    await ctx.respond(random.choice(restart))
    pass


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(tools_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(tools_plugin)