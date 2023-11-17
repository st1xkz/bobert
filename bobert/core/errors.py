import datetime as dt
from datetime import datetime, timedelta
from traceback import format_exception

import hikari
import lightbulb

from bobert.core.utils import chron

errors = lightbulb.Plugin("errors")

"""
@errors.listener(hikari.ExceptionEvent)
async def on_event_error(event: hikari.ExceptionEvent) -> None:
    users = [
        errors.bot.cache.get_user(user)
        for user in [690631795473121280, 994738626816647262]
    ]  # 1: main acc, 2: second acc
    
    try:
        exception = event.exception
    except Exception as exception:
        await event.context.respond(f"Something went wrong during event handling {str(exception)}")
        
        for user in users:
            await user.send(
            	embed=hikari.Embed(
                	title=f"An unexpected `{type(exception).__name__}` occurred",
                    description=f"```py\n{''.join(format_exception(exception.__class__, exception, exception.__traceback__))}```"
                )
            )
        raise exception
"""


@errors.listener(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception
    users = [
        errors.bot.cache.get_user(user)
        for user in [690631795473121280, 994738626816647262]
    ]  # 1: main acc, 2: second acc

    if isinstance(exception, lightbulb.NotOwner):
        embed = hikari.Embed(
            title="Not Owner",
            description=f"You cannot use this command as you are not <@690631795473121280>, but enjoy the rickroll <3",
            color=0xB65E26,
        )
        embed.set_image(
            "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif"
        )
        await event.context.respond(embed=embed)

    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await context.respond(
            f"🚫 This command requires you to either be an Admin or have the `{exception.missing_perms}` permission to use it."
        )

    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            f"{event.context.author.mention}, you're missing an argument for the command `{event.context.command.name}`. You could be missing like **10** and you wouldn't even know. <:pepepoint:993960807090106508>\n\n"
            "**Tip**: Use `/help <command>` for more info on a command",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        cooldown = chron.short_delta(dt.timedelta(seconds=exception.retry_after))
        await event.context.respond(
            f"{event.context.author.mention} Looks like you've been doing that a lot. Take a break for **{cooldown}** before trying again. <:blobpainpats:993961964369875016>",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.OnlyInGuild):
        await event.context.respond("❌ Sorry, this command cannot be used in DMs!")

    elif isinstance(exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`."
        )

        for user in users:
            await user.send(
                embed=hikari.Embed(
                    title=f"An unexpected `{type(exception).__name__}` occurred",
                    description=f"```py\n{''.join(format_exception(exception.__class__, exception, exception.__traceback__))}```",
                )
            )
        raise event.exception
    else:
        raise exception


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors)
