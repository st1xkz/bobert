"""
json to embed converter:
- only prefix command
- owner can only use
"""

import json

import hikari
import lightbulb
import miru

sample = lightbulb.Plugin("sample")
sample.add_checks(lightbulb.checks.owner_only)


class SampleButton(miru.View):
    @miru.button(
        label="Put a label",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="start_support",
    )
    async def sample_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond("Works", flags=hikari.MessageFlag.EPHEMERAL)


@sample.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="sample", description="JSON to embed conversion", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def json_to_embed(ctx: lightbulb.Context) -> None:
    try:
        with open("bobert/sample.json", "r") as file:
            embed_json = json.load(file)
    except FileNotFoundError:
        await ctx.respond("The `sample.json` file was not found.")
        return

    embed = sample.bot.entity_factory.deserialize_embed(embed_json["embed"])
    await ctx.respond(embed=embed, components=SampleButton())


@sample.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    view = SampleButton(timeout=None)
    sample.bot.d.miru.start_view(view)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sample)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sample)
