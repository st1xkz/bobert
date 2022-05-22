import lightbulb

from bobert.core.stuff import to_ascii


ascii_plugin = lightbulb.Plugin("ascii")


@ascii_plugin.command
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
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_ascii(ctx: lightbulb.Context) -> None:
    ascii_text = to_ascii(ctx.options.text)
    if len(ascii_text) < 2000:
        ascii_text = to_ascii(ctx.options.text, True)
        if len(ascii_text) > 2000:
            await ctx.respond("Error: Input is too long", delete_after=10)
            return
        await ctx.respond(ascii_text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ascii_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ascii_plugin)