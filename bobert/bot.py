import asyncio
import os

import aiohttp
import aiosqlite
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
    prefix="*",  # Keep this for sample command
    help_slash_command=True,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
bot.d.miru = miru.Client(bot)


@bot.listen()
async def on_ticket_starting(event: hikari.StartingEvent) -> None:
    async with aiosqlite.connect("bobert/core/utils/db/sql/tickets.db") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS bobert_tickets
            (
                user_id BIGINT,
                channel_id BIGINT
            )
            """
        )
        await db.commit()


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


for folder in os.listdir("bobert/plugins"):
    bot.load_extensions_from("bobert/plugins/" + folder)

bot.load_extensions_from("./bobert/core/", must_exist=True)
bot.load_extensions("lightbulb.ext.filament.exts.superuser")

if os.name != "nt":
    uvloop.install()
