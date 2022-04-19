import hikari
import lightbulb

import time


general_plugin = lightbulb.Plugin("general")


@general_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="ping",
    description="Shows the bot's ping/latency",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping_command(ctx: lightbulb.Context) -> None:
    start = time.perf_counter()
    message = await ctx.respond(
        f"Pong! 🏓 \nWs Latency: **{ctx.bot.heartbeat_latency * 1000:.0f}ms**"
    )
    end = time.perf_counter()

    await message.edit(
        f"Pong! 🏓 \nGateway: **{ctx.bot.heartbeat_latency * 1000:,.0f}ms**\nREST: **{(end-start)*1000:,.0f}ms**"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(general_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(general_plugin)