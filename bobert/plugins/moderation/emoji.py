import hikari
import lightbulb


emoji_plugin = lightbulb.Plugin("emoji")
emoji_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(
        hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS
    )
)


@emoji_plugin.command
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
    name="addemoji",
    aliases=["ae", "me"],
    description="Creates a custom emoji",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_add_emoji(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    img_ext = ("png", "jpg", "gif")

    link_split = ctx.options.message_link.split("/")
    channel = guild.get_channel(int(link_split[5]))
    msg = await ctx.bot.rest.fetch_message(ctx.channel_id, int(link_split[6]))

    if msg.attachments:
        a = msg.attachments[0]
        r = utils.get(a.url)
        img = r.content

        try:
            new_emoji = await guild.create_custom_emoji(
                name=ctx.options.emoji_name,
                image=img,
                reason=f"Emoji has been added by {ctx.user}",
            )

        except hikari.HTTPException as error:
            if "256.0 kb" in str(error):
                return await ctx.edit_original_message(
                    content="Image file too large (Max: 256 kb)"
                )
            return await ctx.edit_original_message(
                content="Error: Could not add the custom emoji to this server"
            )
        return await ctx.edit_original_message(
            content=f"Custom emoji {new_emoji.name} has been created by `{ctx.user}`"
        )
    return await ctx.edit_original_message(
        content="Error: Link did not include a message that had a supported image"
    )


@emoji_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="emoji",
    description="the emoji to be deleted",
    type=hikari.Emoji,
    required=True,
)
@lightbulb.command(
    name="deleteemoji",
    aliases=["de"],
    description="Deletes a specified emoji",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_delete_emoji(ctx: lightbulb.Context) -> None:
    await ctx.respond(f"{ctx.options.emoji} was deleted by `{ctx.user}`")
    await ctx.bot.rest.delete_emoji(ctx.get_guild(), ctx.options.emoji.id)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(emoji_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(emoji_plugin)