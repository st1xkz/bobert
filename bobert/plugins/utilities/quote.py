from datetime import datetime

import hikari
import lightbulb

quote = lightbulb.Plugin("quote")


@quote.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="channel_id",
    description="channel id to get message from",
    type=hikari.GuildChannel,
    required=True,
)
@lightbulb.option(
    name="message_id",
    description="the message to be quoted",
    type=str,
    required=True,
)
@lightbulb.command(
    name="quote",
    description="Quotes a users' message using the message ID and channel ID",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _quote(ctx: lightbulb.Context, message_id: str, channel_id: hikari.GuildChannel) -> None:
    _message_id = int(message_id)
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

    message = await channel_id.fetch_message(_message_id)
    guild_id = message.guild_id
    channel_id = message.channel_id
    message_id = message.id
    jump_url = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"

    embed = hikari.Embed(
        title="Message Link",
        url=f"{jump_url}",
        description=f">>> {message.content}",
        color=color,
        timestamp=datetime.now().astimezone(),
    )
    embed.set_author(name=f"{str(message.author)}", icon=message.author.avatar_url)
    embed.set_footer(text=f"Message quoted by {ctx.author}", icon=ctx.author.avatar_url)
    await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(quote)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(quote)
