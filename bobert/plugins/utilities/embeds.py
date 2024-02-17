import json

import hikari
import lightbulb
import miru

from bobert.core.utils import constants as const

embed = lightbulb.Plugin("embed-editor")

# TODO finish making embed editor command

# Define path to JSON file
# JSON_FILE_PATH = "bobert/core/utils/json_db/embed_data.json"


"""
def load_user_data():
    try:
        with open(JSON_FILE_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Function to save user data to JSON
def save_user_data(user_data):
    with open(JSON_FILE_PATH, "w") as file:
        json.dump(user_data, file)
"""


class ModalOptions(miru.Modal):
    embed_content = (
        miru.TextInput(label="Title's URL", value="Enter a title URL", required=False),
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()

        await ctx.respond("test")


class EmbedEditor(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @miru.button(
        label="Confirm",
        emoji=hikari.Emoji.parse(const.EMOJI_CONFIRM),
        style=hikari.ButtonStyle.SUCCESS,
    )
    async def confirm_button(
        self, ctx: miru.ViewContext, button: miru.Button
    ) -> None: ...

    @miru.button(
        label="Cancel",
        emoji=hikari.Emoji.parse(const.EMOJI_CANCEL),
        style=hikari.ButtonStyle.DANGER,
    )
    async def cancel_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.defer()
        await ctx.edit_response(
            "👍 The embed editor has been cancelled.",
            flags=hikari.MessageFlag.EPHEMERAL,
            components=[],
        )


@embed.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="embed-editor", description="Edits previously sent embeds")
@lightbulb.implements(lightbulb.SlashCommand)
async def embed_management(ctx: lightbulb.Context) -> None:
    modal = ModalOptions("Title")
    builder = modal.build_response(ctx.bot.d.miru)
    view = EmbedEditor()
    embed = hikari.Embed(description="‎")
    await ctx.respond(
        content="### Embed Editor Embed Preview:",
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
        components=view,
    )
    ctx.bot.d.miru.start_view(view)
    await builder.create_modal_response(ctx.interaction)
    ctx.bot.d.miru.start_modal(modal)
    await view.wait()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(embed)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(embed)
