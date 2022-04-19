import hikari
import lightbulb

import os
import sys
import random
from bobert.core.stuff import shutdown, restart


dev_plugin = lightbulb.Plugin("dev")
dev_plugin.add_checks(lightbulb.checks.owner_only)


@dev_plugin.command()
@lightbulb.command(
    name="shutdown",
    aliases=["bye", "fuckoff"],
    description="Shuts the bot down",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_shutdown(ctx: lightbulb.Context) -> None:
    await ctx.respond(random.choice(shutdown))
    await ctx.bot.close()
    await sys.exit()


@dev_plugin.command()
@lightbulb.command(
    name="restart",
    aliases=["hi", "wake"],
    description="Restarts the bot",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_restart(ctx: lightbulb.Context) -> None:
    await ctx.respond(random.choice(restart))
    await ctx.bot.close()
    os.system("clear")
    os.execv(sys.executable, ["python"] + sys.argv)


@dev_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to load",
)
@lightbulb.command(
    name="load",
    description="Loads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_load(ctx: lightbulb.Context) -> None:
    ctx.bot.load_extensions(ctx.options.extension)
    await ctx.respond(
        f"📥 Successfully loaded extension: `{ctx.options.extension}`"
    )


@dev_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to reload",
)
@lightbulb.command(
    name="reload",
    description="Reloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_reload(ctx: lightbulb.Context) -> None:
    ctx.bot.reload_extensions(ctx.options.extension)
    await ctx.respond(
        f"🔄 Successfully reloaded extension: `{ctx.options.extension}`"
    )


@dev_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to unload",
)
@lightbulb.command(
    name="unload",
    description="Unloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_unload(ctx: lightbulb.Context) -> None:
    ctx.bot.unload_extensions(ctx.options.extension)
    await ctx.respond(
        f"📤 Successfully unloaded extension: `{ctx.options.extension}`"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dev_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dev_plugin)