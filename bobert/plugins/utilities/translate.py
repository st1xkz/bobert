import googletrans
import hikari
import lightbulb
import miru
from fuzzywuzzy import fuzz

from bobert.core.stuff.langs import CUSTOM_LANGUAGES
from bobert.core.utils.helpers import detect_language

translate = lightbulb.Plugin("translate")


class TranslateModal(miru.Modal, title="Text Translator"):
    lang = miru.TextInput(
        label="Language",
        placeholder="The language to translate the text into (e.g., English)",
        required=True,
        style=hikari.TextInputStyle.SHORT,
    )
    text = miru.TextInput(
        label="Text",
        placeholder="The text you want to translate (e.g., こんにちは)",
        required=True,
        style=hikari.TextInputStyle.PARAGRAPH,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        language = self.lang.value.strip().lower()
        text = self.text.value.strip()

        language_code = detect_language(language)

        if not language_code:
            closest_match = None
            highest_ratio = 0

            for _, details in CUSTOM_LANGUAGES.items():
                for lang_name in [details[0], details[1]]:
                    ratio = fuzz.ratio(language, lang_name.lower())
                    if ratio > highest_ratio:
                        highest_ratio = ratio
                        closest_match = lang_name

            if closest_match and highest_ratio > 80:
                await ctx.respond(
                    f"Couldn't detect the language you were looking for. Did you mean **{closest_match}**?"
                )
                return

            await ctx.respond(
                f"Sorry, '{language}' is not a valid language. Please try again."
            )
            return

        translator = googletrans.Translator()
        try:
            translations = translator.translate(text, dest=language_code)

            if isinstance(translations, list):
                text_translated = " ".join(
                    [translation.text for translation in translations]
                )
            else:
                text_translated = translations.text

            await ctx.respond(f"{text_translated}")

        except Exception as e:
            raise e


@translate.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="translate",
    description="Translator. Available languages: https://pastebin.com/6SPpG1ed",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def translate_cmd(ctx: lightbulb.SlashContext) -> None:
    modal = TranslateModal()
    builder = modal.build_response(translate.bot.d.miru)

    await builder.create_modal_response(ctx.interaction)

    translate.bot.d.miru.start_modal(modal)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(translate)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(translate)
