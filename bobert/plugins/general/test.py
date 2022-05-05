import hikari
import lightbulb

from datetime import datetime


test_plugin = lightbulb.Plugin("test")


@test_plugin.command
@lightbulb.option(
    name="member",
    description="the member to get the avatar from",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="test",
    description="this is a test command",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand, lightbulb.UserCommand)
async def cmd_test(ctx: lightbulb.UserContext) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    avatar = target.avatar_url or target.default_avatar_url
    if avatar:
        embed = (
            hikari.Embed(
                description=f"{target.mention}'s Avatar",
                timestamp=datetime.now().astimezone(),
            )
            .set_image(
                target.avatar_url or target.default_avatar_url
            )
        )
        await ctx.respond(embed)
    else:
        await ctx.respond(
            "The user you specified doesn't have an avatar set."
        )
        

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(test_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(test_plugin)