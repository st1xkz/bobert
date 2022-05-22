import hikari
import lightbulb

from bobert.core.utils import chron

import time
import platform
import datetime as dt
from datetime import datetime, timedelta
from psutil import Process, virtual_memory


stats_plugin = lightbulb.Plugin("stats")


@stats_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="botinfo",
    aliases=["bot", "stats"],
    description="Displays info about the bot",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_bot(ctx: lightbulb.Context) -> None:
    if not (guild := ctx.get_guild()):
        return

    if not (me := guild.get_my_member()):
        return

    if not (member := ctx.member):
        return

    with (proc := Process()).oneshot():
        uptime = chron.short_delta(
            dt.timedelta(seconds=time.time() - proc.create_time())
        )
        cpu_time = chron.short_delta(
            dt.timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user),
            ms=True,
        )
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
        bot_user = ctx.bot.get_me()

        embed = (
            hikari.Embed(
                title="Statistics for Bobert",
                description=f"""Guild Count: **{len(ctx.bot.cache.get_available_guilds_view())}**
User Count: **{len(ctx.bot.cache.get_users_view())}**
Command Count: **{len(ctx.bot.slash_commands)}**

Uptime: **{uptime}**
CPU Time: **{cpu_time}**
Memory Usage: **{mem_usage:,.3f}/{mem_total:,.0f} MiB ({mem_of_total:,.0f}%)**

Language: **Python**
Python Version: **v{platform.python_version()}**
Library: **hikari-py v{hikari.__version__}**
Command Handler: **hikari-lightbulb v{lightbulb.__version__}**""",
                timestamp=datetime.now().astimezone(),
            )
            .set_thumbnail(
                bot_user.avatar_url or bot_user.default_avatar_url,
            )
            .set_footer(text=f"Bot developed by sticks#5822")
        )
        await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(stats_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(stats_plugin)
