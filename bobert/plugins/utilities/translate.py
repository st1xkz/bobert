import googletrans
import lightbulb
from fuzzywuzzy import fuzz

from bobert.core.stuff.langs import list_of_language

translate = lightbulb.Plugin("translate")


@translate.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to be translated",
    required=True,
)
@lightbulb.option(
    name="language",
    description="the language to be translated from",
    required=True,
)
@lightbulb.command(
    name="translate",
    description="Translator. Available languages: https://pastebin.com/6SPpG1ed",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _translate(ctx: lightbulb.Context, language: str, text: str) -> None:
    lg = language.lower()

    if (
        lg not in googletrans.LANGUAGES
        and lg not in googletrans.LANGCODES
        and lg not in list_of_language
    ):
        for lg in list_of_language:
            if fuzz.ratio(lg, lg) > 80:
                return await ctx.respond(
                    f"Couldn't detect the language you were looking for. Did you mean **{lg}**?"
                )

    text = "".join(text)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lg).text
    await ctx.respond(text_translated)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(translate)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(translate)
