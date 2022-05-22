import hikari
import lightbulb

import textwrap
import inspect
from io import BytesIO


git_plugin = lightbulb.Plugin("git")


@git_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="github",
    aliases=["git"],
    description="Gets the link to the bot's GitHub (you may not copy the bot's code and add it to your own)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_git(ctx: lightbulb.Context) -> None:
    with open("./LICENSE") as f:
        license_ = f.readline().strip()
    await ctx.respond(
        f"<:githubwhite:935336990482772020> This bot is licensed under the **{license_}**\n"
        "https://github.com/st1xkz/bobert"
    )


@git_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="command",
    description="The command to get the source for",
    required=True,
)
@lightbulb.command(
    name="source",
    aliases=["find", "sc"],
    description="Gets source code of any command in the bot (you may not copy the bot's code and add it to your own)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_source(ctx: lightbulb.Context) -> None:
    command = ctx.bot.get_slash_command(ctx.options.command)

    if command is None:
        await ctx.respond(
            "That command doesn't exist.",
            delete_after=10,
        )

    code = textwrap.dedent((inspect.getsource(command.callback)))
    m = await ctx.respond(f"The source code for command `{command.name}`")
    b = BytesIO(code.encode())
    b.seek(0)
    await m.edit(attachment=hikari.Bytes(b, f"source_{command.name}.py"))


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(git_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(git_plugin)
