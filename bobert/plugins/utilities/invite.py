import lightbulb

import asyncio


invite_plugin = lightbulb.Plugin("invite")


@invite_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="channel",
    description="the channel to get",
    required=False,
)
@lightbulb.command(
    name="createinvite",
    aliases=["cin"],
    description="Creates an invite from a specified channel or the current channel",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_invite(ctx: lightbulb.Context) -> None:
    invite = await ctx.bot.rest.create_invite(ctx.options.channel or ctx.get_channel())

    msg = await ctx.respond(
        "Creating your invite link..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content="Setting the duration..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content="Almost got it..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(3)
    await msg.edit(
        content=f"**Done!** Here's your invite: {invite}"
    )
    return


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(invite_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(invite_plugin)