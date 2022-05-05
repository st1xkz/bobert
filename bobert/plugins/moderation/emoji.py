import hikari
import lightbulb


emoji_plugin = lightbulb.Plugin("emoji")

"""
@emoji_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to be deleted",
    type=hikari.Emoji,
    required=True,
)
@lightbulb.command(
    name="deleteemoji",
    aliases=["de"],
    description="Deletes the specified emoji",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_delete_emoji(ctx: lightbulb.Context) -> None:
    if hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS in lightbulb.utils.permissions_for(ctx.member):
        await ctx.respond(
            f"🗑️ Successfully deleted emoji: {ctx.options.emoji}"
        )
        await ctx.bot.rest.delete_emoji(ctx.get_channel(), ctx.options.emoji.id)
"""

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(emoji_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(emoji_plugin)