import lightbulb

from bobert.core.stuff.ascii import to_ascii

ascii = lightbulb.Plugin("ascii")


@ascii.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to send",
    required=True,
)
@lightbulb.command(
    name="ascii",
    description="Converts text to ASCII",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _ascii(ctx: lightbulb.Context, text: str) -> None:
    ascii_text = to_ascii(text)
    if len(ascii_text) < 2000:
        ascii_text = to_ascii(text, True)
        if len(ascii_text) > 2000:
            await ctx.respond(
                "❌ Input is too long. Your text must be less than 2000 characters.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return
        await ctx.respond(ascii_text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ascii)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ascii)
