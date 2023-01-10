import lightbulb

ext = lightbulb.Plugin("ext")
ext.add_checks(lightbulb.checks.owner_only)


@ext.command
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
    choices=[
        "admin",
        "fun",
        "general",
        "information",
        "listeners",
        "moderation",
        "utilities",
    ],
)
@lightbulb.command(
    name="load",
    description="Loads an extension",
    pass_options=True,
    hidden=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def extension_load(ctx: lightbulb.Context, category: str, name: str) -> None:
    try:
        load = ctx.bot.load_extensions(f"bobert.plugins.{category}.{name}")
        await ctx.respond(f"📥 Successfully loaded extension: `{name}`")
    except:
        await ctx.respond(
            "⚠️ This extension has already been loaded, has not been unloaded yet, or does not exist.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


@ext.command
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
    choices=[
        "admin",
        "fun",
        "general",
        "information",
        "listeners",
        "moderation",
        "utilities",
    ],
)
@lightbulb.command(
    name="reload",
    description="Reloads an extension",
    pass_options=True,
    hidden=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def extension_reload(ctx: lightbulb.Context, category: str, name: str) -> None:
    ctx.bot.reload_extensions(f"bobert.plugins.{category}.{name}")
    await ctx.respond(f"🔄 Successfully reloaded extension: `{name}`")


@ext.command
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
    choices=[
        "admin",
        "fun",
        "general",
        "information",
        "listeners",
        "moderation",
        "utilities",
    ],
)
@lightbulb.command(
    name="unload",
    description="Unloads an extension",
    pass_options=True,
    hidden=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def extension_unload(ctx: lightbulb.Context, category: str, name: str) -> None:
    try:
        unload = ctx.bot.unload_extensions(f"bobert.plugins.{category}.{name}")
        await ctx.respond(f"📤 Successfully unloaded extension: `{name}`")
    except:
        await ctx.respond(
            "⚠️ This extension has already been unloaded, has not been loaded yet, or does not exist.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
