import inspect
import random
from datetime import datetime

import hikari
import lightbulb

from bobert.bot import bot
from bobert.core.stuff.langs import langs
from bobert.core.utils import chron


class Help(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, ctx: lightbulb.Context) -> None:
        """This is triggered when /help is invoked"""
        lg = random.choice(langs)

        embed = (
            hikari.Embed(
                description="""Welcome to Bobert's help!
Find all the categories available on this panel. """,
                color=0xEBDBB2,
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                "Categories:",
                "f",
            )
            .set_author(
                name=f"{lg} {ctx.author.username}!",
                icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
            )
            .set_image(
                "https://cdn.discordapp.com/attachments/993704075419992154/995907703866138694/bobert_help_menu.png"
            )
            .set_thumbnail(
                ctx.bot.get_me().avatar_url or ctx.bot.get_me().default_avatar_url
            )
            .set_footer(text=f"Requested by {ctx.author}")
        )
        await ctx.respond(embed=embed)

    async def send_plugin_help(
        self, ctx: lightbulb.Context, pi: lightbulb.Plugin
    ) -> None:
        """This is triggered when /help <plugin> is invoked"""
        pass

    async def send_group_help(self, ctx: lightbulb.Context, grp) -> None:
        """This is triggered when /help <group> is invoked"""
        pass

    async def send_command_help(
        self, ctx: lightbulb.Context, cmd: lightbulb.Command
    ) -> None:
        """This is triggered when /help <command> is invoked"""
        desc = f"```ini\n[ {cmd.description} ]\n```\n"
        embed = (
            hikari.Embed(
                color=0xEBDBB2,
                description=desc
                + (inspect.getdoc(cmd.callback) or "No additional details provided."),
            )
            .add_field(name="Usage:", value=f"```{cmd.signature}```")
            .set_author(
                name=f"{cmd.name.upper()} COMMAND",
                icon=self.bot.get_me().avatar_url
                or self.bot.get_me().default_avatar_url,
            )
            .set_footer(
                f"Requested by {ctx.author}",
                icon=ctx.author.avatar_url or ctx.author.default_avatar_url,
            )
        )
        await ctx.respond(embed=embed)

    async def object_not_found(self, ctx: lightbulb.Context, obj) -> None:
        """If command is not found, send message for confirmation"""
        await ctx.respond(
            f"❌ No command or category with the name `{obj}` could be found."
        )


help = lightbulb.Plugin("help")


@help.listener(hikari.MessageCreateEvent)
async def mention_bot_help(event: hikari.MessageCreateEvent) -> None:
    """This is triggered when the bot is mentioned"""
    bot = help.bot
    cd = chron.long_date_and_short_time(bot.get_me().created_at)
    lg = random.choice(langs)

    if event.message.content == bot.get_me().mention:
        embed = (
            hikari.Embed(
                title="Bobert Help!",
                description=f"""Hello! I'm Bobert, the official utility and moderation bot for Sage. To use me, type `/help` or `/help [command/category]` for more info on a command or category. *In total, I have **{len(bot.slash_commands)}** commands.*

Where commands have parameters, they are formatted like this:
```\n[optional] <required>\n```
**...**
As this command just provides information on how to use me, you should get in touch with  [**the developer**](https://discord.com/users/690631795473121280) for more detailed assistance and information.""",
                color=0xEBDBB2,
                timestamp=datetime.now().astimezone(),
            )
            .set_author(
                name=f"{lg} {event.author.username}!",
                icon=event.author.avatar_url or event.author.default_avatar_url,
            )
            .set_thumbnail(bot.get_me().avatar_url or bot.get_me().default_avatar_url)
            .set_footer(
                text=f"Bobert was created on {cd}",
                icon=bot.get_me().avatar_url or bot.get_me().default_avatar_url,
            )
        )
        await event.message.respond(embed=embed, reply=True, mentions_reply=True)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(help)
    bot.d.old_help_command = bot.help_command
    bot.help_command = Help(bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(help)
    bot.help_command = bot.d.old_help_command
    del bot.d.old_help_command
