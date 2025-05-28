import asyncio
import os

import hikari
import lightbulb
import miru
import uvloop
from dotenv import load_dotenv
from lightbulb.ext import tasks

load_dotenv()

token = os.getenv("TOKEN")

if not token:
    raise ValueError("TOKEN environment variable not set")


bot = lightbulb.BotApp(
    token=token,
    banner="bobert",
    prefix="*",  # Keep for sample and eval command
    help_slash_command=True,
    ignore_bots=True,
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
bot.d.miru = miru.Client(bot)


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
