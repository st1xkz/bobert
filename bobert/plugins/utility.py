import hikari
import lightbulb

from bobert.core.stuff import list_of_language

import io
import asyncio
import aiohttp
import googletrans
from PIL import Image
from fuzzywuzzy import fuzz
from datetime import datetime
from simpleeval import simple_eval


utility_plugin = lightbulb.Plugin("utility")


"""
@plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("name", "what you want to call the emoji")
@lightbulb.option("url", "url of emoji")
@lightbulb.command(name="createemoji", aliases=["ce"], description="Creates a server emoji")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ce_command(ctx: lightbulb.Context) -> None:
"""


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("emoji", "the emoji to be deleted", hikari.Emoji)
@lightbulb.command(name="deleteemoji", aliases=["de"], description="Deletes the specified emoji")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def de_command(ctx: lightbulb.Context) -> None:
    if hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS in lightbulb.utils.permissions_for(ctx.member):
        await ctx.respond(
            f"Successfully deleted emoji: {ctx.options.emoji}"
        )
        await ctx.options.emoji.RESTClient.delete_emoji()


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("channel", "The channel to get", required=False)
@lightbulb.command(name="createinvite", aliases=["cin"], description="Creates an invite from a specified channel or the current channel")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cin_command(ctx: lightbulb.Context) -> None:
    invite = await ctx.bot.rest.create_invite(ctx.options.channel or ctx.get_channel())

    msg = await ctx.respond(
        "Creating your invite link..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content="Setting the duration..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content="Almost got it..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content=f"**Done!** Here's your invite: {invite}"
    )
    return


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("reminder", "The reminder to be sent", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("time", "The time to set")
@lightbulb.command(name="remind", aliases=["rem"], description="Sets a reminder (default duration is 5 mins)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def remind_command(ctx: lightbulb.Context) -> None:
    seconds = 0
    if ctx.options.reminder is None:
        await ctx.respond(
            "Please specify what do you want me to remind you about.",
            delete_after=10
        )
        
    if ctx.options.time.lower().endswith("d"):
        seconds += int(ctx.options.time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if ctx.options.time.lower().endswith("h"):
        seconds += int(ctx.options.time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif ctx.options.time.lower().endswith("m"):
        seconds += int(ctx.options.time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif ctx.options.time.lower().endswith("s"):
        seconds += int(ctx.options.time[:-1])
        counter = f"{seconds} seconds"
        
    if seconds == 0:
        await ctx.respond(
            "Please specify a proper duration, type `*help remind` for more information.",
            delete_after=10
        )
    elif seconds < 300:
        await ctx.respond(
            "The minimum duration is 5 minutes.",
            delete_after=10
        )
    elif seconds > 7776000:
        await ctx.respond(
            "The maximum duration is 90 days.",
            delete_after=10
        )
    else:
        embed = hikari.Embed(
            title="Reminder Set 🔔",
            description=f"Alright {ctx.author.username}, your reminder for \"{ctx.options.reminder}\" has been set and will end in {counter}.",
            timestamp=datetime.now().astimezone()
        )
        await ctx.respond(
            embed,
            reply=True,
            mentions_reply=True
        )
        await asyncio.sleep(seconds)

        embed = hikari.Embed(
            title="Reminder 🔔",
            description=f"Hi, you asked me to remind you about \"{ctx.options.reminder}\" {counter} ago.",
            color=0x2f3136,
            timestamp=datetime.now().astimezone()
        )
        await ctx.author.send(embed)
        return


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("hex_code", "The hex code to the specified color", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="getcolor", aliases=["color", "gc"], description="Displays color of specified hex code (you can add up to 10)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def color_command(ctx: lightbulb.Context) -> None:
    color_codes = ctx.options.hex_code.split()
    size = (60, 80) if len(color_codes) > 1 else (200, 200)
    
    if len(color_codes) > 10:
        return await ctx.respond(
            "You can only supply a maximum of **10** hex codes.",
            delete_after=10
        )
        
    for color_code in color_codes:
        if not color_code.startswith("#"):
            colour_code = "#" + color_code
            image = Image.new("RGB", size, colour_code)
            buf = io.BytesIO()

            with buf as file:
                image.save(file, "PNG")
                file.seek(0)
                
                embed = (
                    hikari.Embed(
                        title=f"Color `{colour_code}`",
                        color=0x2f3136,
                        timestamp=datetime.now().astimezone(),
                    )
                    .set_image(
                        hikari.Bytes(file, "Color.png")
                    )
                    .set_footer(
                        text=f"Requested by {ctx.author}"
                    )
                )
                await ctx.respond(embed)
            await asyncio.sleep(1)


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to be translated", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("language", "The language to be translated from")
@lightbulb.command(name="translate", aliases=["lang", "tr"], description="Translator. [Available languages](https://pastebin.com/6SPpG1ed)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def translate_command(ctx: lightbulb.Context) -> None:
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


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("emoji", "The emoji to be enlarged", hikari.Emoji)
@lightbulb.command(name="enlarge", aliases=["jumbo"], description="Enlarges a specified emoji")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def emoji_command(ctx: lightbulb.Context) -> None:
    if type(ctx.options.emoji) is str:
        emoji_id = ord(ctx.options.emoji[0])
        await ctx.respond(
            f"https://twemoji.maxcdn.com/v/latest/72x72/{emoji_id:x}.png"
        )
    else:
        await ctx.respond(ctx.options.emoji.url)


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User, required=False)
@lightbulb.command(name="avatar", aliases=["ava"], description="Displays the avatar of a Discord member or yours")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def avatar_command(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)
    
    embed = hikari.Embed(
        title=f"{target.username}#{target.discriminator}'s Avatar",
        timestamp=datetime.now().astimezone()
    )
    embed.set_image(target.avatar_url or target.default_avatar_url)
    await ctx.respond(embed)


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("channel_id" , "Channel id to get message from" , lightbulb.converters.special.GuildChannelConverter)
@lightbulb.option("message_id", "The message to be be quoted", type=int)
@lightbulb.command(name="quote", aliases=["qu"], description="Quotes a users' message using the message ID and channel ID")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def quote_command(ctx: lightbulb.Context) -> None:
    message = await ctx.options.channel_id.fetch_message(ctx.options.message_id)
    guild_id = message.guild_id
    channel_id = message.channel_id
    message_id = message.id
    jump_url = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

    embed = (
        hikari.Embed(
            title="Message Link",
            url=f"{jump_url}",
            description=f">>> {message.content}",
            timestamp=datetime.now().astimezone(),
        )
        .set_author(
            name=f"{str(message.author)}",
            icon=message.author.avatar_url
        )
        .set_footer(
            text=f"Message quoted by {ctx.author}",
            icon=ctx.author.avatar_url
        )
    )
    await ctx.respond(embed)


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("equation", "The equation to be evaluated", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="calculator", aliases=["calc", "eval"], description="Calculator.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def calc_command(ctx: lightbulb.Context) -> None:
    expr = ctx.options.equation
    solution = simple_eval(ctx.options.equation)

    embed = (
        hikari.Embed(
            title="Calculator",
            color=0xffffff,
        )
        .add_field(
            "Input",
            f"```py\n{expr}\n```",
            inline=False,
        )
        .add_field(
            "Output",
            f"```py\n{solution}\n```",
            inline=False
        )
    )
    await ctx.respond(embed)


@utility_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("word", "The word to be defined")
@lightbulb.command(name="define", aliases=["d"], description="Defines a word")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def define_command(ctx: lightbulb.Context) -> None:
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/en_US/{ctx.options.word}"
        )

    if response.status == 404:
        return await ctx.respond(
            f'No word called "{ctx.options.word}" found.',
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

    async with ctx.get_channel().trigger_typing():
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
                f'"{example}"',
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
    bot.add_plugin(utility_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(utility_plugin)