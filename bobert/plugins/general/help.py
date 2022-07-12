import hikari
import lightbulb

import random
from bobert.bot import bot
from bobert.core.utils import chron
from bobert.core.stuff import langs
from datetime import datetime

"""
class Help(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, ctx: lightbulb.Context) -> None:
        pass

    async def send_plugin_help(self, ctx: lightbulb.Context, plugin: lightbulb.Plugin) -> None:
        pass

    async def send_command_help(self, ctx: lightbulb.Context, cmd: lightbulb.Command) -> None:
        pass

    async def object_not_found(self, ctx: lightbulb.Context, obj) -> None:
        pass
"""

help_plugin = lightbulb.Plugin("custom help")


@help_plugin.listener(hikari.MessageCreateEvent)
async def mention_bot_help(event: hikari.MessageCreateEvent) -> None:
    bot = help_plugin.bot
    cd = chron.short_date_and_time(bot.created_at)
    langs = random.choice(langs)
    color = (
        c[0] if (c := [r.color for r in bot.get_roles() if r.color != 0]) else None
    )

    if event.message == bot:
        embed = (
            hikari.Embed(
                title="Bobert Help!",
                description=f"""Hello! I'm Bobert, the official utility and moderation for Sage. To use me, type `*help` for a list of commands and categories. If you want more info on a specific command, type `*help [command]`, and `*help [category]` for more info on a category. *In total, I have **{len(bot.slash_commands)}** commands; I have slash commands and am also mentionable.*

Where commands have parameters, they are formatted like this:
```
[optional] <required>
```
**...**
For more in-depth help and info in regards to using me, you should contact <@690631795473121280> (developer) as this command only shows information about how to use me.""",
                color=color,
                timestamp=datetime.utc().astimezone(),
            )
            .set_author(
                name=f"{langs} {event.author.nickname}!",
                icon=event.author.avatar_url or event.author.default_avatar_url
            )
            .set_thumbnail(f"{bot.avatar_url}")
            .set_footer(text=f"Bobert was created on {cd}", icon=bot.avatar_url)
        )
        await event.message.respond(embed, reply=True, mentions_reply=True)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(help_plugin)
    # bot.d.old_help_command = bot.help_command
    # bot.help_command = Help(bot)


def unload(bot: lightbulb.BotApp) -> None:
     bot.remove_plugin(help_plugin)
    # bot.help_command = bot.d.old_help_command
    # del bot.d.old_help_command