import googletrans
import hikari
import lightbulb

from bobert.core.stuff.langs import CUSTOM_LANGUAGES
from bobert.core.utils import helpers
from bobert.core.utils.helpers import detect_language

context = lightbulb.Plugin("context")


@context.command
@lightbulb.command(
    name="Show avatar",
    description="Shows your own or another user's avatar",
)
@lightbulb.implements(lightbulb.UserCommand)
async def show_avatar_ctx(ctx: lightbulb.UserContext) -> None:
    target = ctx.bot.cache.get_member(ctx.guild_id, ctx.options.target.id)  # type: ignore

    if not target:
        await ctx.respond(
            "❌ The user you specified isn't in the server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    color = (
        c[0]
        if (c := [r.color for r in helpers.sort_roles(target.get_roles()) if r.color])
        else None
    )

    at = "Server" if target.guild_avatar_url else "Global"

    embed = hikari.Embed(
        title=f"{target}",
        description=f"[**{at} Avatar URL**]({target.display_avatar_url})",
        color=color,
    )
    embed.set_image(target.display_avatar_url)
    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@context.command
@lightbulb.command(
    name="Detect Language",
    description="Detect the language of the provided text",
)
@lightbulb.implements(lightbulb.MessageCommand)
async def detect_message_ctx(ctx: lightbulb.MessageContext) -> None:
    text = ctx.options.target.content

    custom_lang_code = detect_language(text)
    if custom_lang_code:
        language_name = CUSTOM_LANGUAGES[custom_lang_code][0]
        return

    translator = googletrans.Translator()
    detection = translator.detect(text)

    if not detection or not detection.lang:
        await ctx.respond(
            "Sorry, I couldn't detect the language of the provided text.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    language_name = googletrans.LANGUAGES.get(detection.lang, "Unknown").capitalize()

    await ctx.respond(
        f"The language detected from the provided text is **{language_name} ({detection.lang.upper()})**.",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(context)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(context)
