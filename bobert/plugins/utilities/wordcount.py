import lightbulb


word_count_plugin = lightbulb.Plugin("word count")


@word_count_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="word count",
    description="Displays the word count for the specified message",
)
@lightbulb.implements(lightbulb.MessageCommand)
async def cmd_word_count(ctx: lightbulb.MessageContext) -> None:
    message = ctx.options.target
    words = len(message.content.split(" "))
    await ctx.respond(f"**Message**: {message.content}\n" f"**Word Count**: {words:,}")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(word_count_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(word_count_plugin)
