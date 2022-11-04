import inspect
import os

import hikari
import lightbulb

source = lightbulb.Plugin("source")


@source.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="cmd",
    description="the command to get the source for",
    type=str,
    required=False,
)
@lightbulb.command(
    name="source",
    description="Displays link to the bot's GitHub or to a specific command",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def source(ctx: lightbulb.Context, cmd: str) -> None:
    _cmd = ctx.bot.get_slash_command(cmd)
    source_url = "https://github.com/st1xkz/bobert"
    branch = "main"

    with open("./LICENSE") as f:
        license_ = f.readline().strip()
        if not _cmd:
            await ctx.respond(f"<{source_url}>")
            return

        if _cmd == "help":
            src = type(ctx.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = ctx.bot.get_slash_command(cmd.replace(".", " "))
            if obj is None:
                return await ctx.respond(f"Could not find command called `{_cmd}`.")

            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            if filename is None:
                return await ctx.respond(f"Could not find source for command `{_cmd}`.")

            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"

        await ctx.respond(
            f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(source)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(source)
