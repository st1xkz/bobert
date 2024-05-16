import json
import os

import hikari
import lightbulb

api = lightbulb.Plugin("api")


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

    async with api.bot.d.aio_session.get(
        f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_KEY')}"
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
