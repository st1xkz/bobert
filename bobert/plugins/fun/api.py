import os
from random import randint

import hikari
import lightbulb

api = lightbulb.Plugin("api")

NASA_KEY = os.environ["NASA_KEY"]


@api.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="rok",
    description="It's a rok",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def rok(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://mrconos.pythonanywhere.com/rock/random"
    ) as res:
        data = await res.json()
    rok_name = data["name"]
    rok_desc = data["desc"]
    rok_img = data["image"]

    embed = hikari.Embed(
        title=rok_name,
        description=rok_desc,
        color=randint(0, 0xFFFFFF),
    )
    if not rok_img == "none":
        embed.set_image(rok_img)
    await ctx.respond(embed=embed)


@api.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="random-fact",
    description="Random facts everyday",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def random_fact(ctx: lightbulb.Context) -> None:
    params = {
        "type": "json",
    }

    async with ctx.bot.d.aio_session.get(
        "https://api.popcat.xyz/fact",
        params=params,
    ) as res:
        data = await res.json()
    fact = data["fact"]

    embed = hikari.Embed(
        title="Random Fact",
        description=f"{fact}",
        color=0x090828,
    )
    embed.set_image(
        "https://media.discordapp.net/attachments/900458968588120154/976717764746166272/IMG_3302.gif"
    )
    await ctx.respond(embed=embed)


@api.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="apod",
    description="NASA's Astronomy Picture of the Day",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def apod(ctx: lightbulb.Context) -> None:
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    async with ctx.bot.d.aio_session.get(
        f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}"
    ) as res:
        data = await res.json()
    apod_title = data["title"]
    apod_date = data["date"]
    apod_desc = data["explanation"]
    apod_image = data["url"]

    embed = hikari.Embed(
        title="Astronomy Picture of the Day",
        color=color,
        description=apod_desc,
    )
    embed.set_image(apod_image)
    embed.set_footer(text=f"{apod_title} | {apod_date}")
    await ctx.respond(embed=embed)


@api.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="dad-joke",
    description="An unlimited supply of Dad Jokes!",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def dad_joke(ctx: lightbulb.Context) -> None:
    headers = {
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com",
        "X-RapidAPI-Key": "34ee5096eamsh85d7e98f3aa03c0p1ffaa0jsn527481c4e4a7",
        "Accept": "application/json",
    }

    async with ctx.bot.d.aio_session.get(
        "https://dad-jokes.p.rapidapi.com/random/joke",
        headers=headers,
    ) as res:
        data = await res.json()
    setup = data.get("body")[0].get("setup")
    punchline = data.get("body")[0].get("punchline")

    await ctx.respond(f"{setup}\n\n{punchline}")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(api)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(api)
