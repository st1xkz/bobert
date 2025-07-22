import json

import aiofiles
import hikari
import lightbulb
import miru

from bobert.plugins.listeners.ticket import TicketButton

sample = lightbulb.Plugin("sample")


class SampleButton(miru.View):
    @miru.button(
        label="Start Support",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="start_support",
    )
    async def sample_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond(TicketButton)

"""
class SampleSelect(miru.View):
    @miru.text_select(
        placeholder="Choose a position...",
        options=[
            miru.SelectOption(label="Event Planner", emoji="🎉"),
            miru.SelectOption(label="Event Assistant", emoji="📋"),
            miru.SelectOption(label="Trainee", emoji="🛡️"),
        ],
        custom_id="sample_roles",
    )
    async def select_menu(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        role = select.values[0]
        modal = AppModal(role)  # Use the modal from app.py
        await ctx.respond_with_modal(modal)
"""

"""
        try:
            print(f"Select menu triggered with value: {select.values}")
            role = select.values[0]
            print(f"Selected role: {role}")
        except Exception as e:
            print(f"Error handling select menu: {str(e)}")  # Debugging statement
            await ctx.respond(
                "An error occurred while handling your selection.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
"""


@sample.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="sample", description="JSON to embed conversion", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def json_to_embed(ctx: lightbulb.Context) -> None:
    try:
        async with aiofiles.open("bobert/sample.json", "r") as file:
            content = await file.read()
            embed_json = json.loads(content)

    except FileNotFoundError:
        await ctx.respond("The `sample.json` file was not found.")
        return

    embed = sample.bot.entity_factory.deserialize_embed(embed_json["embed"])
    button_view = SampleButton()
    # select_view = SampleSelect()

    # Send the embed with button
    # await ctx.respond(embed=embed, components=button_view)

    # Send the select menu separately
    await ctx.respond(embed=embed, components=button_view)


@sample.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    button_view = SampleButton(timeout=None)
    # select_view = SampleSelect(timeout=None)
    sample.bot.d.miru.start_view(button_view)
    # sample.bot.d.miru.start_view(select_view)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sample)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sample)