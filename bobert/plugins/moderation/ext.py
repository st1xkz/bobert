import hikari
import lightbulb


ext_plugin = lightbulb.Plugin("ext")
@ext_plugin.add_checks(lightbulb.checks.owner_only)


@ext_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to load",
)
@lightbulb.command(
    name="load",
    description="Loads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_load(ctx: lightbulb.Context) -> None:
    ctx.bot.load_extensions(ctx.options.extension)
    await ctx.respond(
        f"📥 Successfully loaded extension: `{ctx.options.extension}`"
    )


@ext_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to reload",
)
@lightbulb.command(
    name="reload",
    description="Reloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_reload(ctx: lightbulb.Context) -> None:
    ctx.bot.reload_extensions(ctx.options.extension)
    await ctx.respond(
        f"🔄 Successfully reloaded extension: `{ctx.options.extension}`"
    )


@ext_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="extension",
    description="the extension to unload",
)
@lightbulb.command(
    name="unload",
    description="Unloads an extension",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_unload(ctx: lightbulb.Context) -> None:
    ctx.bot.unload_extensions(ctx.options.extension)
    await ctx.respond(
        f"📤 Successfully unloaded extension: `{ctx.options.extension}`"
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ext_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ext_plugin)