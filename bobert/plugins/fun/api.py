import os

import aiohttp
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
async def apod_cmd(ctx: lightbulb.SlashContext) -> None:
    member = ctx.member

    if member:
        color = (
            c[0]
            if (c := [r.color for r in member.get_roles() if r.color != 0])
            else None
        )

    url = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('NASA_KEY')}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                else:
                    await ctx.respond(
                        "Failed to fetch the Astronomy Picture of the Day.",
                        flags=hikari.MessageFlag.EPHEMERAL,
                    )
                    return
        except aiohttp.ClientError:
            await ctx.respond(
                "An error occurred while fetching the Astronomy Picture of the Day.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

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
