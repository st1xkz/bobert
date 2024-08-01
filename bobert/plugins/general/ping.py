import time

import lightbulb

ping = lightbulb.Plugin("ping")


@ping.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="ping",
    description="Displays the ping/latency of the bot",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def ping_cmd(ctx: lightbulb.Context) -> None:
    start = time.perf_counter()
    message = await ctx.respond(
        f"Pong! 🏓 \n" f"Ws Latency: **{ctx.bot.heartbeat_latency * 1000:.0f}ms**"
    )
    end = time.perf_counter()

    await message.edit(
        f"Pong! 🏓 \n"
        f"Gateway: **{ctx.bot.heartbeat_latency * 1000:,.0f}ms**\n"
        f"REST: **{(end-start)*1000:,.0f}ms**"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ping)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ping)
