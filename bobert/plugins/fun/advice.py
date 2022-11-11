import json

import lightbulb

advice = lightbulb.Plugin("advice")


@advice.command
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(advice)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(advice)
