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
async def enlarge_emoji(ctx: lightbulb.Context, emoji: hikari.Emoji) -> None:
    _emoji = hikari.Emoji.parse(emoji)
    await ctx.respond(_emoji.url)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(enlarge)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(enlarge)
