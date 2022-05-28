import asyncio
from datetime import datetime

import hikari
import lightbulb

remind_plugin = lightbulb.Plugin("remind")


@remind_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reminder",
    description="the reminder to be sent",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="time",
    description="the time to set",
    required=True,
)
@lightbulb.command(
    name="remind",
    aliases=["rem"],
    description="Sets a reminder (default duration is 5 mins)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_remind(ctx: lightbulb.Context) -> None:
    seconds = 0
    if ctx.options.reminder is None:
        await ctx.respond(
            "Please specify what do you want me to remind you about.", delete_after=10
        )

    if ctx.options.time.lower().endswith("d"):
        seconds += int(ctx.options.time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if ctx.options.time.lower().endswith("h"):
        seconds += int(ctx.options.time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif ctx.options.time.lower().endswith("m"):
        seconds += int(ctx.options.time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif ctx.options.time.lower().endswith("s"):
        seconds += int(ctx.options.time[:-1])
        counter = f"{seconds} seconds"

    if seconds == 0:
        await ctx.respond(
            "Please specify a proper duration, type `*help remind` for more information.",
            delete_after=10,
        )
    elif seconds < 300:
        await ctx.respond("The minimum duration is 5 minutes.", delete_after=10)
    elif seconds > 7776000:
        await ctx.respond("The maximum duration is 90 days.", delete_after=10)
    else:
        embed = hikari.Embed(
            title="Reminder Set 🔔",
            description=f'Alright {ctx.author.username}, your reminder for "{ctx.options.reminder}" has been set and will end in {counter}.',
            timestamp=datetime.now().astimezone(),
        )
        await ctx.respond(embed, reply=True, mentions_reply=True)
        await asyncio.sleep(seconds)

        embed = hikari.Embed(
            title="Reminder 🔔",
            description=f'Hi, you asked me to remind you about "{ctx.options.reminder}" {counter} ago.',
            color=0x2F3136,
            timestamp=datetime.now().astimezone(),
        )
        await ctx.author.send(embed)
        return


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(remind_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(remind_plugin)
