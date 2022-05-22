import hikari
import lightbulb

from simpleeval import simple_eval


calc_plugin = lightbulb.Plugin("calc")


@calc_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="equation",
    description="the equation to be evaluated",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="calculator",
    aliases=["calc", "eval"],
    description="Calculator.",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_calc(ctx: lightbulb.Context) -> None:
    expr = ctx.options.equation
    solution = simple_eval(ctx.options.equation)

    embed = (
        hikari.Embed(
            title="Calculator",
            color=0xFFFFFF,
        )
        .add_field(
            "Input",
            f"```py\n{expr}\n```",
            inline=False,
        )
        .add_field("Output", f"```py\n{solution}\n```", inline=False)
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(calc_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(calc_plugin)