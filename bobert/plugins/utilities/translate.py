import googletrans
import lightbulb
from fuzzywuzzy import fuzz

from bobert.core.stuff.langs import CUSTOM_LANGUAGES

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
async def translate_cmd(ctx: lightbulb.Context, language: str, text: str) -> None:
    lg = language.lower()

    list_of_language = [lang[0].lower() for lang in CUSTOM_LANGUAGES.values()]

    if (
        lg not in googletrans.LANGUAGES
        and lg not in googletrans.LANGCODES
        and lg not in list_of_language
    ):
        closest_match = None
        highest_ratio = 0

        for lang in list_of_language:
            ratio = fuzz.ratio(lg, lang)
            if ratio > highest_ratio:
                highest_ratio = ratio
                closest_match = lang

        if closest_match and highest_ratio > 80:
            await ctx.respond(
                f"Couldn't detect the language you were looking for. Did you mean **{closest_match}**?"
            )
            return

    text = "".join(text)
    translator = googletrans.Translator()
    translations = translator.translate(text, dest=lg)

    if isinstance(translations, list):
        text_translated = " ".join([translation.text for translation in translations])
    else:
        text_translated = translations.text

    await ctx.respond(text_translated)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(translate)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(translate)
