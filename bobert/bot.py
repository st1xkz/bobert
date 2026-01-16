import asyncio
import os

import hikari
import lightbulb
import miru
from dotenv import load_dotenv
from lightbulb.ext import tasks

import bobert.core
import bobert.plugins

load_dotenv()

token = os.getenv("TOKEN")

if not token:
    raise ValueError("TOKEN environment variable not set")


bot = hikari.GatewayBot(
    token=token,
    banner="bobert",
    intents=hikari.Intents.ALL,
)
tasks.load(bot)
bot.d.miru = miru.Client(bot)


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    await client.load_extensions_from_package(bobert.core, recursive=True)
    await client.load_extensions_from_package(bobert.plugins, recursive=True)

    await client.start()


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
