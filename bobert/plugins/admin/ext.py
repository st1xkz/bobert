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
    load = ctx.bot.load_extensions(f"bobert.plugins.{category}.{name}")

    if load:
        await ctx.respond(f"📥 Successfully loaded extension: `{name}`")
    else:
        await ctx.respond(
            "⚠️ This extension has already been loaded or it does not exist."
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
    unload = ctx.bot.unload_extensions(f"bobert.plugins.{category}.{name}")

    if unload:
        await ctx.respond(f"📤 Successfully unloaded extension: `{name}`")
    else:
        await ctx.respond(
            "⚠️ This extension has already been unloaded or it does not exist."
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ext)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext)
