import hikari
import lightbulb
import miru

plugin = lightbulb.Plugin("EmbedEditor")


class EditEmbed(miru.View):
    def __init__(
        self, bot: hikari.GatewayBot, original_embed: hikari.Embed, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.original_embed = original_embed
        self.preview_embed = hikari.Embed(
            title=original_embed.title,
            description=original_embed.description,
            url=original_embed.url,
            color=original_embed.color,
            timestamp=original_embed.timestamp,
            author=original_embed.author,
            footer=original_embed.footer,
            image=original_embed.image,
            thumbnail=original_embed.thumbnail,
            fields=list(original_embed.fields),
        )

    @miru.text_select(
        options=[
            miru.SelectOption(
                label="Title & Description", value="edit_title_description"
            ),
            miru.SelectOption(label="Color", value="edit_color"),
            miru.SelectOption(label="Fields", value="edit_fields"),
            miru.SelectOption(label="Image/Thumbnail", value="edit_image_thumbnail"),
        ],
        placeholder="What do you want to edit?",
        custom_id="edit_options",
    )
    async def edit_menu(
        self, interaction: miru.ViewContext, select: miru.TextSelect
    ) -> None:
        selection = select.values[0]
        await interaction.respond(
            f"You selected: {selection}", flags=hikari.MessageFlag.EPHEMERAL
        )


@plugin.command
@lightbulb.option(
    name="message_id",
    description="The ID of the message containing the embed",
    type=hikari.Snowflake,
    required=True,
)
@lightbulb.option(
    name="channel_id",
    description="The ID of the channel where the message is",
    type=hikari.Snowflake,
    required=True,
)
@lightbulb.command(name="edit-embed", description="Edits an existing embed")
@lightbulb.implements(lightbulb.SlashCommand)
async def edit_embed(ctx: lightbulb.SlashContext) -> None:
    try:
        message = await ctx.bot.rest.fetch_message(
            ctx.options.channel_id, ctx.options.message_id
        )
    except hikari.NotFoundError:
        await ctx.respond("Error: Message not found.")
        return

    if not message.embeds:
        await ctx.respond("Error: The specified message does not contain any embeds.")
        return

    original_embed = message.embeds[0]
    view = EditEmbed(ctx.bot, original_embed, timeout=300)
    response_message = await ctx.respond(
        embed=view.preview_embed,
        components=view.build(),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
    ctx.bot.d.miru.start_view(view, bind_to=response_message)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
