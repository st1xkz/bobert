import hikari
import lightbulb


class Help(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, ctx):
        pass

    async def send_plugin_help(self, ctx, plugin):
        pass

    async def send_command_help(self, ctx, cmd):
        pass

    async def send_group_help(self, ctx, group):
        pass

    async def object_not_found(self, ctx, obj):
        pass


def load(bot: lightbulb.BotApp) -> None:
    bot.d.old_help_command = bot.help_command
    bot.help_command = Help(bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.help_command = bot.d.old_help_command
    del bot.d.old_help_command