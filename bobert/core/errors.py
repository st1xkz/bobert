import hikari
import lightbulb

from traceback import format_exception

errors_plugin = lightbulb.Plugin("errors")


@errors_plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception
    users = [
        errors_plugin.bot.cache.get_user(user) for user in [690631795473121280, 994738626816647262]
    ]  # 1: main, 2: second

    if isinstance(exception, lightbulb.NotOwner):
        embed = hikari.Embed(
            title="Not Owner",
            description=f"You cannot use this command as you are not <@690631795473121280>, but enjoy the rickroll <3",
            color=0xB65E26,
        )
        embed.set_image(
            "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif"
        )
        await event.context.respond(embed)

    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        embed = hikari.Embed(
            title="<:no:993686064805978182> Missing Permissions",
            description=f"This command requires you to either be an Admin or have the `{exception.missing_perms}` permission to use it.",
            color=0x2F3136,
        )
        await event.context.respond(embed)

    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            f"{event.context.author.mention}, you're missing an argument for the command `{event.context.command.name}`. You could be missing like **10** and you wouldn't even know. <:pepepoint:993960807090106508>\n\n"
            "**Tip**: Use `*help <command>` for more info on a command",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"{event.context.author.mention} Looks like you've been doing that a lot. Take a break for **{exception.retry_after:.2f}s** before trying again. <:blobpainpats:993961964369875016>",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.OnlyInGuild):
        await event.context.respond(
            "<:no:993686064805978182> Sorry, this command cannot be used in DMs!"
        )

    elif isinstance(exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`."
        )
# TODO: fix this error message
# and fix slash commands displaying twice
# Will fix when back to America **
        for user in users:
            await event.context.respond(
                embed = hikari.Embed(
                    title=f"An unexpected `{type(exception).__name__}` occurred",
                    description=f"```py\n{''.join(format_exception(exception.__class__, exception, exception.__traceback__))}```"
                )
            )
        raise event.exception
    else:
        raise exception


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors_plugin)
