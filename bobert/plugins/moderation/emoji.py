import hikari
import lightbulb

emoji = lightbulb.Plugin("emoji")
emoji.add_checks(
    lightbulb.checks.has_guild_permissions(
        hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS
    )
)


@emoji.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="message_link",
    type=str,
    description="the message link of the attachment",
    required=True,
)
@lightbulb.option(
    name="emoji_name",
    type=str,
    description="what you want to call the emoji",
    required=True,
)
@lightbulb.command(
    name="add-emoji",
    description="Creates a custom emoji",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def add_emoji(ctx: lightbulb.Context, emoji_name: str, message_link: str) -> None:
    guild = ctx.get_guild()

    link_split = message_link.split("/")
    msg = await ctx.bot.rest.fetch_message(ctx.channel_id, int(link_split[6]))

    if msg.attachments:
        a = msg.attachments[0]
        url = a.url

        res = await ctx.bot.d.aio_session.get(url)
        bytes_data = await res.read()

        try:
            new_emoji = await ctx.bot.rest.create_emoji(
                name=emoji_name,
                guild=guild,
                image=bytes_data,
                reason=f"Emoji has been added via command",
            )

        except hikari.BadRequestError as error:
            if "256.0 kb" in str(error):
                return await ctx.respond(content="Image file too large (Max: 256 kb)")
            return await ctx.respond(
                content="❌ Error: Could not add the custom emoji to this server"
            )
        return await ctx.respond(
            content=f"👍 Custom emoji {new_emoji} ({new_emoji.name}) has been created by `{ctx.user}`"
        )
    return await ctx.respond(
        content="❌ Error: Link did not include a message that had a supported image"
    )


@emoji.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to be deleted",
    type=hikari.CustomEmoji,
    required=True,
)
@lightbulb.command(
    name="delete-emoji",
    description="Deletes a specified emoji",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_emoji(ctx: lightbulb.Context, emoji: hikari.CustomEmoji) -> None:
    await ctx.respond(f"👍 {emoji} was deleted by `{ctx.user}`")
    _emoji = await lightbulb.EmojiConverter(ctx).convert(emoji)
    await ctx.bot.rest.delete_emoji(ctx.get_guild(), _emoji)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(emoji)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(emoji)
