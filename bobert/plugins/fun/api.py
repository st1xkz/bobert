import os
from random import randint

import hikari
import lightbulb

api_plugin = lightbulb.Plugin("api")

my_secret = os.environ["NASA"]


@api_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="rok",
    description="It's a rok",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_rok(ctx: lightbulb.Context) -> None:
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
        await ctx.respond(embed)


@api_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="randomfact",
    aliases=["rf"],
    description="Random facts everyday",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_random_fact(ctx: lightbulb.Context) -> None:
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
    await ctx.respond(embed)


@api_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="apod",
    description="NASA's Astronomy Picture of the Day",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_apod(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        f"https://api.nasa.gov/planetary/apod?api_key={my_secret}"
    ) as res:
        data = await res.json()

    apod_title = data["title"]
    apod_date = data["date"]
    apod_desc = data["explanation"]
    apod_image = data["url"]

    embed = hikari.Embed(
        title="Astronomy Picture of the Day",
        description=apod_desc,
    )
    embed.set_image(apod_image)
    embed.set_footer(text=f"{apod_title} | {apod_date}")
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(api_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(api_plugin)
