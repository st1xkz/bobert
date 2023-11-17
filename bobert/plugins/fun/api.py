import json
import os

import hikari
import lightbulb

api = lightbulb.Plugin("api")


@api.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="advice",
    description="Don't be afraid to ask for advice!",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _advice(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(f"https://api.adviceslip.com/advice") as res:
        data = json.loads(await res.read())
    adv = data["slip"]["advice"]
    await ctx.respond(adv)


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
        f"https://api.nasa.gov/planetary/apod?api_key=EJJKg8XzGlJtqqOzyoKpw1mknrQsogj9xliM8mjJ"
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(api)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(api)
