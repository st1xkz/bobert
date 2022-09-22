import hikari
import lightbulb

enlarge_emoji_plugin = lightbulb.Plugin("emoji")


@enlarge_emoji_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to be enlarged",
    type=hikari.Emoji,
    required=True,
)
@lightbulb.command(
    name="enlarge",
    aliases=["jumbo"],
    description="Enlarges a specified emoji",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_emoji(ctx: lightbulb.Context) -> None:
    if type(ctx.options.emoji) is str:
        emoji_id = ord(ctx.options.emoji[0])
        await ctx.respond(f"https://twemoji.maxcdn.com/v/latest/72x72/{emoji_id:x}.png")
    else:
        await ctx.respond(ctx.options.emoji.url)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(enlarge_emoji_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(enlarge_emoji_plugin)
