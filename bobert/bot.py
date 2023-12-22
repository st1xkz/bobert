import asyncio
import os

import aiohttp
import asyncpg
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
    banner="bobert",
    help_slash_command=True,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
miru.install(bot)


@bot.listen()
async def on_ticket_starting(event: hikari.StartingEvent) -> None:
    bot.d.ticket_pool = await asyncpg.create_pool(os.environ["PGSQL_TICKET_HOST"])
    bot.d.aio_ticket_session = aiohttp.ClientSession()

    await bot.d.ticket_pool.execute(
        """
        CREATE TABLE IF NOT EXISTS bobert_tickets
        (
            user_id BIGINT,
            channel_id BIGINT
        );
        """
    )


@bot.listen()
async def on_levels_starting(event: hikari.StartingEvent) -> None:
    print("on_levels_starting event is triggered")
    bot.d.levels_pool = await asyncpg.create_pool(os.environ.get["PGSQL_LEVELS_HOST"])
    bot.d.aio_levels_session = aiohttp.ClientSession()

    await bot.d.levels_pool.execute(
        """
        CREATE TABLE IF NOT EXISTS bobert_levels
        (
        	user_id BIGINT PRIMARY KEY,
            xp INT DEFAULT 0,
            level INT DEFAULT 0,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    print("table created: bobert_levels")


@bot.listen()
async def on_levels_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_levels_session.close()


@bot.listen()
async def on_ticket_stopping(event: hikari.StoppingEvent) -> None:
    await bot.d.aio_ticket_session.close()


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
    await asyncio.sleep(600)
    await bot.update_presence(
        activity=hikari.Activity(
            name="Adventure Time | hikari is love hikari is life ❤️",
            type=hikari.ActivityType.WATCHING,
        )
    )


for folder in os.listdir("bobert/plugins"):
    bot.load_extensions_from("bobert/plugins/" + folder)

bot.load_extensions_from("./bobert/core/", must_exist=True)

if os.name != "nt":
    uvloop.install()
