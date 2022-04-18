import hikari
import lightbulb
import miru

import asyncio
from lightbulb.ext import tasks
import aiohttp
from main import my_secret
from bobert.core.utils.color_logs import *


bot = lightbulb.BotApp(
    token=my_secret,
    banner=None,
    default_enabled_guilds=(900458404953333808, 870013765071028285), # first one is test server, second one is cloverfield
    prefix=lightbulb.when_mentioned_or(";"),
    help_slash_command=True,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
miru.load(bot)


@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.aio_session = aiohttp.ClientSession()

@bot.listen()
async def on_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_session.close()

@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    update_presence.start()


@tasks.task(m=5, auto_start=True)
async def update_presence() -> None:
    await bot.update_presence(
        activity=hikari.Activity(
            name="Adventure Time | ping me for help",
            type=hikari.ActivityType.WATCHING,
        )
    )
    await asyncio.sleep(300)
    await bot.update_presence(
        activity=hikari.Activity(
            name=f"Adventure Time | {len(bot.slash_commands)} commands",
            type=hikari.ActivityType.WATCHING,
        )
    )
    await asyncio.sleep(300)
    await bot.update_presence(
        activity=hikari.Activity(
            name="Adventure Time | I'm the best bot ever made",
            type=hikari.ActivityType.WATCHING,
        )
    )
    await asyncio.sleep(300)
    await bot.update_presence(
        activity=hikari.Activity(
            name="Adventure Time | hikari is love hikari is life ❤️",
            type=hikari.ActivityType.WATCHING,
        )
    )


bot.load_extensions_from("./bobert/plugins/", must_exist=True)
bot.load_extensions_from("./bobert/core/meta/", must_exist=True)
bot.load_extensions_from("./bobert/core/meta/debug/", must_exist=True)

bot.run()