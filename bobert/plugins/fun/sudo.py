import hikari
import lightbulb

sudo_plugin = lightbulb.Plugin("sudo")


@sudo_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to send",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="sudo",
    description="Puts words into other peoples mouth's",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_sudo(ctx: lightbulb.Context) -> None:
    for k in await ctx.bot.rest.fetch_guild_webhooks(ctx.guild_id):
        if k.author == ctx.author:
            await k.delete()
    webhook = await ctx.bot.rest.create_webhook(
        name=f"{ctx.options.member}", channel=ctx.channel_id
    )

    await webhook.execute(
        ctx.options.text,
        username=ctx.options.member.username,
        avatar_url=ctx.options.member.avatar_url
        or ctx.options.member.default_avatar_url,
        mentions_everyone=False,
        user_mentions=False,
        role_mentions=False,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sudo_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sudo_plugin)
