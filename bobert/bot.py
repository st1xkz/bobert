import asyncio
import os

import aiohttp
import aiosqlite
import asyncpg
import hikari
import lightbulb
import miru
import uvloop
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from lightbulb.ext import tasks

from bobert.core.utils import color_logs
from bobert.db.init_db import create_pool, init_db

load_dotenv()


bot = lightbulb.BotApp(
    token=os.getenv("TOKEN"),
    banner="bobert",
    prefix="*",  # Keep for sample and eval command
    help_slash_command=True,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
bot.d.miru = miru.Client(bot)
scheduler = AsyncIOScheduler()


@bot.listen()
async def on_start(event: hikari.StartingEvent):
    bot.d.pool = await create_pool()
    await init_db(bot.d.pool)
    print("Database initialized and pool created")


@bot.listen()
async def on_close(event: hikari.StoppingEvent):
    await bot.d.pool.close()
    print("Database pool closed")


@bot.listen()
async def on_started(event: hikari.StartedEvent) -> None:
    update_presence.start()


@tasks.task(m=10, auto_start=True)
async def update_presence() -> None:
    await bot.update_presence(
        status=hikari.Status.IDLE,
        activity=hikari.Activity(
            name="Adventure Time | /help",
            type=hikari.ActivityType.WATCHING,
        ),
    )
    await asyncio.sleep(600)
    await bot.update_presence(
        activity=hikari.Activity(
            name=f"Adventure Time | {len(bot.slash_commands)} commands",
            type=hikari.ActivityType.WATCHING,
        )
    )
    await asyncio.sleep(600)
    await bot.update_presence(
        activity=hikari.Activity(
            name="Adventure Time | I'm the best bot ever made",
            type=hikari.ActivityType.WATCHING,
        )
    )


for folder in os.listdir("bobert/plugins"):
    bot.load_extensions_from("bobert/plugins/" + folder)

bot.load_extensions_from("./bobert/core/", must_exist=True)

if os.name != "nt":
    uvloop.install()
