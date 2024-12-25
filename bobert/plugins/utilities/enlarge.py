import hikari
import lightbulb

enlarge = lightbulb.Plugin("emoji")


@enlarge.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to be enlarged",
    type=hikari.Emoji,
    required=True,
)
@lightbulb.command(
    name="enlarge",
    description="Enlarges a specified emoji",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def enlarge_cmd(ctx: lightbulb.SlashContext, emoji: hikari.Emoji) -> None:
    await ctx.respond(emoji.url)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(enlarge)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(enlarge)
