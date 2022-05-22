import hikari
import lightbulb

from random import randint


api_plugin = lightbulb.Plugin("api")


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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(api_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(api_plugin)
