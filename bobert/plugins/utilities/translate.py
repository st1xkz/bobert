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
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="language",
    description="the language to be translated from",
    required=True,
)
@lightbulb.command(
    name="translate",
    description="Translator. [Available languages](https://pastebin.com/6SPpG1ed)",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _translate(ctx: lightbulb.Context, language: str, text: str) -> None:
    language = language.lower()

    if (
        language not in googletrans.LANGUAGES
        and language not in googletrans.LANGCODES
        and language not in list_of_language
    ):
        for language in list_of_language:
            if fuzz.ratio(language, language) > 80:
                return await ctx.respond(
                    f"Couldn't detect the language you were looking for. Did you mean... `{language}`?"
                )

    text = "".join(text)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=language).text
    await ctx.respond(text_translated)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(translate)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(translate)
