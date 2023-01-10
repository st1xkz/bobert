from datetime import datetime

import hikari
import lightbulb

quote = lightbulb.Plugin("quote")


@quote.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="channel",
    description="the channel where the message is in",
    type=hikari.GuildChannel,
    required=True,
)
@lightbulb.option(
    name="message_id",
    description="the message id of the message you want to quote",
    type=str,
    required=True,
)
@lightbulb.command(
    name="quote",
    description="Uses the message ID and channel to quote a user's message",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _quote(
    ctx: lightbulb.Context, message_id: str, channel: hikari.GuildChannel
) -> None:
    """Allows mentioning of a channel or to use the id of one when using the channel option."""
    _message_id = int(message_id)
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    message = await ctx.bot.rest.fetch_message(channel.id, _message_id)
    guild_id = message.guild_id
    _channel = message.channel_id
    message_id = message.id
    jump_url = f"https://discord.com/channels/{guild_id}/{_channel}/{message_id}"

    embed = hikari.Embed(
        title="Message Link",
        url=f"{jump_url}",
        description=f">>> {message.content}",
        color=color,
        timestamp=datetime.now().astimezone(),
    )
    embed.set_author(
        name=f"{str(message.author)}",
        icon=message.author.avatar_url or message.author.default_avatar_url,
    )
    embed.set_footer(
        text=f"Message quoted by {ctx.author}",
        icon=message.author.avatar_url or message.author.default_avatar_url,
    )
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(quote)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(quote)
