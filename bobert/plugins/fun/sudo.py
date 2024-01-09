import hikari
import lightbulb

sudo = lightbulb.Plugin("sudo")


@sudo.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to send",
    required=True,
)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="sudo",
    description="Fills other people's mouths with words",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _sudo(ctx: lightbulb.Context, member: hikari.Member, text: str) -> None:
    """Allows mentioning of a member or to use their ID when using the member option."""
    for k in await ctx.bot.rest.fetch_guild_webhooks(ctx.guild_id):
        if k.author == ctx.author:
            await k.delete()
    webhook = await ctx.bot.rest.create_webhook(
        name=f"{member}", channel=ctx.channel_id
    )

    await webhook.execute(
        text,
        username=member.username,
        avatar_url=member.display_avatar_url,
        mentions_everyone=False,
        user_mentions=False,
        role_mentions=False,
    )
    await ctx.respond(
        "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sudo)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sudo)
