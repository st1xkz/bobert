from datetime import datetime

import hikari
import lightbulb

quote_plugin = lightbulb.Plugin("quote")


@quote_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="channel_id",
    description="channel id to get message from",
    type=lightbulb.converters.special.GuildChannelConverter,
    required=True,
)
@lightbulb.option(
    name="message_id",
    description="the message to be be quoted",
    type=int,
    required=True,
)
@lightbulb.command(
    name="quote",
    aliases=["qu"],
    description="Quotes a users' message using the message ID and channel ID",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_quote(ctx: lightbulb.Context) -> None:
    member = ctx.member
    color = c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    
    message = await ctx.options.channel_id.fetch_message(ctx.options.message_id)
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
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(quote_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(quote_plugin)
