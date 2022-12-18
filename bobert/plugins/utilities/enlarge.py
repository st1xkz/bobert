import hikari
import lightbulb

enlarge = lightbulb.Plugin("emoji")

# FIXME: find out why it only sends a link when specifying a custom emoji but works fine for regular emoji
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
    if type(emoji) is str:
        emoji_id = ord(emoji[0])
        await ctx.respond(f"https://twemoji.maxcdn.com/v/latest/72x72/{emoji_id:x}.png")
    else:
        await ctx.respond(emoji.url)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(enlarge)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(enlarge)
