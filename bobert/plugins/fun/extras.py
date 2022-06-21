import random
from random import randint

import hikari
import lightbulb

from bobert.core.stuff import sites, text_to_owo

extras_plugin = lightbulb.Plugin("extras")


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="what do you want to pay respect to?",
    type=str,
    required=False,
    modifier=lightbulb.commands.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="f",
    description="Press F to pay respect.",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_f(ctx: lightbulb.Context) -> None:
    hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]
    reason = f"for **{ctx.options.text}** " if ctx.options.text else ""
    await ctx.respond(
        f"**{ctx.author.username}** has paid their respect {reason}{random.choice(hearts)}"
    )


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="digits",
    description="the number of digits to send",
    type=int,
    required=True,
)
@lightbulb.command(
    name="randomnumber",
    aliases=["rn"],
    description="Generates a random number with the specified length of digits",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_number(ctx: lightbulb.Context) -> None:
    number = ""

    for i in range(ctx.options.digits):
        number += str(random.randint(0, 9))
    await ctx.respond(number)


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to be sent",
    required=True,
)
@lightbulb.command(
    name="reverse",
    aliases=["rev"],
    description="Reverses text",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_reverse(ctx: lightbulb.Context) -> None:
    t_rev = ctx.options.text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.respond(t_rev)


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="useless",
    aliases=["uls"],
    description="Gives you a random/useless website",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_useless(ctx: lightbulb.Context) -> None:
    randomsite = random.choice(sites)
    embed = hikari.Embed(
        title="Here's your useless website:",
        description=f"🌐 {randomsite}",
        color=randint(0, 0xFFFFFF),
    )
    await ctx.respond(embed)


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to send",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="owo",
    description="Turns text to owo (e.g. hewwo)",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_owo(ctx: lightbulb.Context) -> None:
    await ctx.respond(text_to_owo(ctx.options.text))


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="pp",
    description="Checks the size of someone's pp",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_pp(ctx: lightbulb.Context) -> None:
    ctx.options.member = ctx.author
    pp = [
        "8D",
        "8=D",
        "8==D",
        "8===D",
        "8====D",
        "8=====D",
        "8======D",
        "8=======D",
        "8========D",
        "8=========D",
        "8==========D",
        "8===========D",
        "8============D",
        "8=============D",
    ]

    if ctx.options.member:
        embed = hikari.Embed(
            title=f"{ctx.options.user.mention}'s pp:",
            description=f"{random.choice(pp)}",
        )
        await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title=f"Your pp:",
            description=f"{random.choice(pp)}",
        )
        await ctx.respond(embed)


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="question",
    description="the question to be asked",
    required=True,
)
@lightbulb.command(
    name="8ball",
    description="Wisdom. Ask a question and the bot will give you an answer",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_8ball(ctx: lightbulb.Context) -> None:
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes – definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don’t count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful.",
    ]
    await ctx.respond(f"{random.choice(responses)}")


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="bonus",
    description="a fixed number to add to the total roll",
    type=int,
    default=0,
)
@lightbulb.option(
    name="sides",
    description="the number of sides each die will have",
    type=int,
    default=6,
)
@lightbulb.option(
    name="number",
    description="the number of dice to roll",
    type=int,
)
@lightbulb.command(
    name="dice",
    description="Roll one or more dice",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_dice(ctx: lightbulb.Context) -> None:
    number = ctx.options.number
    sides = ctx.options.sides
    bonus = ctx.options.bonus

    if number > 25:
        await ctx.respond(
            "No more than 25 dice can be rolled at once.", delete_after=10
        )
        return

    if sides > 100:
        await ctx.respond("The dice cannot have more than 100 sides.", delete_after=10)
        return

    rolls = [random.randint(1, sides) for _ in range(number)]

    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to repeat",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="echo",
    aliases=["say"],
    description="Repeats the user's input",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(extras_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(extras_plugin)
