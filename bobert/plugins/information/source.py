import inspect
import os

import hikari
import lightbulb

source_plugin = lightbulb.Plugin("source")


@source_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="command",
    description="the command to get the source for",
    required=False,
)
@lightbulb.command(
    name="source",
    aliases=["src"],
    description="Displays link to the bot's GitHub or to a specific command",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_source(ctx: lightbulb.Context) -> None:
    command = ctx.bot.get_slash_command(ctx.options.command)
    source_url = "https://github.com/st1xkz/bobert"
    branch = "main"

    with open("./LICENSE") as f:
        license_ = f.readline().strip()
        if not ctx.options.command:
            embed = (
                hikari.Embed(
                    title="Bot's GitHub Repository",
                    description=f"This bot is licensed under the **{license_}**",
                )
                .add_field(
                    "Repository",
                    f"[Go to repo]({source_url})",
                )
                .set_thumbnail(
                    "https://cdn.discordapp.com/attachments/900458968588120154/982515431011123230/IMG_1413.png"
                )
            )
            await ctx.respond(embed)
            return

        if ctx.options.command == "help":
            src = type(ctx.bot.help_command)
            module = src.__module__
            filename = inspect.getsourcefile(src)
        else:
            obj = ctx.bot.get_slash_command(ctx.options.command.replace(".", " "))
            if obj is None:
                return await ctx.respond(
                    f"Could not find command called `{ctx.options.command}`."
                )

            src = obj.callback.__code__
            module = obj.callback.__module__
            filename = src.co_filename

        lines, firstlineno = inspect.getsourcelines(src)
        if not module.startswith("discord"):
            if filename is None:
                return await ctx.respond(
                    f"Could not find source for command `{ctx.options.command}`."
                )

            location = os.path.relpath(filename).replace("\\", "/")
        else:
            location = module.replace(".", "/") + ".py"

        final_url = f"<{source_url}/blob/{branch}/{location}#L{firstlineno}-L{firstlineno + len(lines) - 1}>"
        embed = (
            hikari.Embed(
                title=f"Command: {ctx.options.command}",
                description=f"{command.description}",
            )
            .add_field("Source Code", f"[Go to repo]({final_url})")
            .set_footer(
                text=f"{location}, line #{firstlineno}-{firstlineno + len(lines)-1}"
            )
        )
        await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(source_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(source_plugin)
