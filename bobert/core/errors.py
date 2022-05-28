import lightbulb

errors_plugin = lightbulb.Plugin("errors")


@errors_plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception

    if isinstance(exception, lightbulb.NotOwner):
        await event.context.respond("You're not the owner of this bot, are you? 🤨")

    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        await event.context.respond(
            f"🚫 This command requires you to either be an Admin or have the `{exception.missing_perms}` permission to use it.",
            reply=True,
            mentions_reply=True,
        )

    elif isinstance(exception, lightbulb.NotEnoughArguments):
        await event.context.respond(
            f"{event.context.author.mention}, you're missing an argument for the command `{event.context.command.name}`. You could be missing like **10** and you wouldn't even know. <:pepepoint:935318313741991976>\n\n"
            "**Tip**: Use `*help <command>` for more info on a command",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(
            f"{event.context.author.mention} Looks like you've been doing that a lot. Take a break for **{exception.retry_after:.2f}s** before trying again. <:blobpainpats:903057516345303060>",
            user_mentions=True,
        )

    elif isinstance(exception, lightbulb.OnlyInGuild):
        await event.context.respond("Sorry, this command cannot be used in DMs!")

    elif isinstance(exception, lightbulb.CommandInvocationError):
        await event.context.respond(
            f"Something went wrong during invocation of command `{event.context.command.name}`."
        )
        raise event.exception
    else:
        raise exception


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(errors_plugin)
