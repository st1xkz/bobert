import random
from random import randint

import hikari
import lightbulb

from bobert.core.stuff import sites

extras = lightbulb.Plugin("extras")


@extras.command
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
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_f(ctx: lightbulb.Context, text: str) -> None:
    hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]
    reason = f"for **{text}** " if text else ""
    await ctx.respond(
        f"**{ctx.author.username}** has paid their respect {reason}{random.choice(hearts)}"
    )


@extras.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="digits",
    description="the number of digits to send",
    type=int,
    required=True,
)
@lightbulb.command(
    name="random-number",
    description="Generates a random number with the specified length of digits",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_number(ctx: lightbulb.Context, digits: int) -> None:
    number = ""

    for i in range(digits):
        number += str(random.randint(0, 9))
    await ctx.respond(number)


@extras.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="useless",
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
    await ctx.respond(embed=embed)


@extras.command
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(extras)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(extras)
