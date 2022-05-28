import hikari
import lightbulb

roast_plugin = lightbulb.Plugin("roast")


@roast_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the member to roast",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="roast",
    description="Roast your friends! (Some jokes might be offensive)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_roast(ctx: lightbulb.Context) -> None:
    params = {
        "type": "json",
    }

    async with ctx.bot.d.aio_session.get(
        "https://evilinsult.com/generate_insult.php",
        params=params,
    ) as res:
        data = await res.json()
    insult = data["insult"]

    await ctx.respond(content=f"{ctx.options.member.mention}, {insult}")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(roast_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(roast_plugin)
