import random
from random import randint

import hikari
import lightbulb

from bobert.core.stuff import sites

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
@lightbulb.implements(lightbulb.SlashCommand)
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
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_number(ctx: lightbulb.Context) -> None:
    number = ""

    for i in range(ctx.options.digits):
        number += str(random.randint(0, 9))
    await ctx.respond(number)


@extras_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="useless",
    aliases=["uls"],
    description="Gives you a random/useless website",
)
@lightbulb.implements(lightbulb.SlashCommand)
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
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="pp",
    description="Checks the size of someone's pp",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_pp(ctx: lightbulb.Context) -> None:
    ctx.options.member = ctx.author

    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

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
            color=color,
        )
        await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title=f"Your pp:",
            description=f"{random.choice(pp)}",
            color=color,
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
@lightbulb.implements(lightbulb.SlashCommand)
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
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_echo(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(extras_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(extras_plugin)
