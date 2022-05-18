import hikari
import lightbulb

from random import randint


api_plugin = lightbulb.Plugin("api's")


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
            color=randint(0, 0xffffff),
        )
        if not rok_img == "none":
            embed.set_image(rok_img)
        await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(api_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(api_plugin)