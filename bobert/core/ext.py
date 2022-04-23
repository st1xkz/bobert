import hikari
import lightbulb


ext_plugin = lightbulb.Plugin("ext")
@ext_plugin.add_checks(lightbulb.checks.owner_only)


@ext_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="name",
    description="the name of the extension",
    type=str,
    required=True,
    modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="category",
    description="the category of the extension",
    type=str,
    required=True,
    choices=["fun", "general", "information",
             "moderation", "utilities",],
)
@lightbulb.command(
    name="load",
    description="Loads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_load(ctx: lightbulb.Context) -> None:
    ctx.bot.load_extensions(f"bobert.plugins.{ctx.options.category}.{ctx.options.name}")
    await ctx.respond(
        f"📥 Successfully loaded extension: `{ctx.options.name}`"
    )


@ext_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="name",
    description="the name of the extension",
    type=str,
    required=True,
    modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="category",
    description="the category of the extension",
    type=str,
    required=True,
    choices=["fun", "general", "information",
             "moderation", "utilities",],
)
@lightbulb.command(
    name="reload",
    description="Reloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_reload(ctx: lightbulb.Context) -> None:
    ctx.bot.reload_extensions(f"bobert.plugins.{ctx.options.category}.{ctx.options.name}")
    await ctx.respond(
        f"🔄 Successfully reloaded extension: `{ctx.options.name}`"
    )


@ext_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="name",
    description="the name of the extension",
    type=str,
    required=True,
    modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="category",
    description="the category of the extension",
    type=str,
    required=True,
    choices=["fun", "general", "information",
             "moderation", "utilities",],
)
@lightbulb.command(
    name="unload",
    description="Unloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_unload(ctx: lightbulb.Context) -> None:
    ctx.bot.unload_extensions(f"bobert.plugins.{ctx.options.category}.{ctx.options.name}")
    await ctx.respond(
        f"📤 Successfully unloaded extension: `{ctx.options.name}`"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ext_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext_plugin)