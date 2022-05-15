import lightbulb


dm_plugin = lightbulb.Plugin("dm")


@dm_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to be sent",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.option(
    "user_id",
    "The user's ID",
    required=False,
)
@lightbulb.command(
    name="dm",
    description="DMs given user through the bot",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_dm(ctx: lightbulb.Context) -> None:
    user = ctx.bot.cache.get_user(ctx.options.user_id)
    if user:
        await user.send(ctx.options.text)
        await ctx.respond(
        f"Your message has been sent to the specified user! ({user.mention})"
    )
    else:
        await ctx.respond(
            "I cannot DM the user you specified."
        )


@dm_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="the text to be sent",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="dmall",
    description="DMs all users in the server through the bot",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_dmall(ctx: lightbulb.Context) -> None:
    if ctx.options.text != None:
        for member in ctx.get_guild().get_members().keys():
            if member == ctx.bot.get_me().id: continue
            await ctx.get_guild().get_member(member).send(ctx.options.text)
            
        await ctx.respond(
            "Your message has been sent to everyone!"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(dm_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(dm_plugin)