from datetime import datetime
from random import randint

import hikari
import lightbulb

meme = lightbulb.Plugin("meme")


@meme.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="meme",
    description="Shows a random Reddit meme",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _meme(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://meme-api.herokuapp.com/gimme"
    ) as response:
        res = await response.json()

        if response.ok and res["nsfw"] != True:
            link = res["postLink"]
            title = res["title"]
            img_url = res["url"]

            embed = (
                hikari.Embed(
                    title=title,
                    color=randint(0, 0xFFFFFF),
                    timestamp=datetime.now().astimezone(),
                    url=link,
                )
                .set_author(
                    name=f"{ctx.author.username}#{ctx.author.discriminator}",
                    icon=ctx.author.avatar_url,
                )
                .set_image(img_url)
                .set_footer(text="Here is your meme!")
            )
            await ctx.respond(embed=embed)

        else:
            await ctx.respond(
                "Could not fetch a meme :c", flags=hikari.MessageFlag.EPHEMERAL
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(meme)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(meme)
