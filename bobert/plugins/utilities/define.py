import hikari
import lightbulb

import aiohttp
from datetime import datetime


define_plugin = lightbulb.Plugin("define")


@define_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="word",
    description="the word to be defined",
    required=True,
)
@lightbulb.command(
    name="define",
    aliases=["d"],
    description="Defines a word",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_define(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{ctx.options.word}"
        )

    if response.status == 404:
        return await ctx.respond(
            f"No word called \"{ctx.options.word}\" found.",
            reply=True,
            mentions_reply=True,
            delete_after=10
        )

    wordx = await response.json()
    the_dictionary = wordx[0]
    meanings = the_dictionary["meanings"]
    definitions = meanings[0]
    definition = definitions["definitions"]
    meaningg = definition[0]
    meaning = meaningg["definition"]
    example = meaningg.get("example", "None")
    synlist = meaningg.get("synonyms", "None")

    if isinstance(synlist, str):
        synlist = synlist
    synlist = ", ".join(synlist)

    if not synlist:
        synlist = "None"

    embed = (
        hikari.Embed(
            title=f"`{ctx.options.word.lower()}`",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Definition:",
            f"{meaning}",
            inline=False,
        )
        .add_field(
            "Example:",
            f"\"{example}\"",
            inline=False,
        )
        .add_field(
            "Synonyms:",
            f"`{synlist}`",
            inline=False,
        )
        .set_thumbnail(
            "https://cdn.discordapp.com/attachments/900458968588120154/912960931284267068/oed_sharing.png"
            )
        .set_footer(
            text=f"Oxford Dictionaries: definition for {ctx.options.word.lower()}"
        )
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(define_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(define_plugin)