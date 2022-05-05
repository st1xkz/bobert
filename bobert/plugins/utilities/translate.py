import lightbulb

import googletrans
from fuzzywuzzy import fuzz
from bobert.core.stuff.langs import list_of_language


translate_plugin = lightbulb.Plugin("translate")


@translate_plugin.command
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
    aliases=["lang", "tr"],
    description="Translator. [Available languages](https://pastebin.com/6SPpG1ed)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_translate(ctx: lightbulb.Context) -> None:
    language = ctx.options.language.lower()
    
    if language not in googletrans.LANGUAGES and language not in googletrans.LANGCODES and language not in list_of_language:
        for language in list_of_language:
            if fuzz.ratio(ctx.options.language, language) > 80:
                return await ctx.respond(
                    f"Couldn't detect the language you were looking for. Did you mean... `{language}`?"
                )
                
    text = ''.join(ctx.options.text)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=language).text
    await ctx.respond(text_translated)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(translate_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(translate_plugin)