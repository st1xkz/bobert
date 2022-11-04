import lightbulb

from bobert.core.stuff import to_ascii

ascii = lightbulb.Plugin("ascii")


@ascii.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to send",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="ascii",
    description="Turns text to ascii",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def ascii(ctx: lightbulb.Context, text: str) -> None:
    ascii_text = to_ascii(text)
    if len(ascii_text) < 2000:
        ascii_text = to_ascii(text, True)
        if len(ascii_text) > 2000:
            await ctx.respond("Error: Input is too long", delete_after=10)
            return
        await ctx.respond(ascii_text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ascii)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ascii)
