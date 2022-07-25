import asyncio
import os

import aiohttp
import hikari
import lightbulb
import miru
import uvloop
from dotenv import load_dotenv
from lightbulb.ext import tasks

from bobert.core.utils import color_logs

load_dotenv()
bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    banner="assets",
    prefix=lightbulb.when_mentioned_or(";"),
    help_slash_command=True,
    case_insensitive_prefix_commands=True,
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


for folder in os.listdir("bobert/plugins"):
    bot.load_extensions_from("bobert/plugins/" + folder)

bot.load_extensions_from("./bobert/core/", must_exist=True)
bot.load_extensions("lightbulb.ext.filament.exts.superuser")

if os.name != "nt":
    uvloop.install()
