import hikari
import lightbulb
import miru


class SussyButton(miru.View):
    @miru.button(label="Click Me!", emoji=hikari.Emoji.parse("<:catok:987098283455418379>"), style=hikari.ButtonStyle.PRIMARY)
    async def sussy_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond("https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif", flags=hikari.MessageFlag.EPHEMERAL)


sus_plugin = lightbulb.Plugin("sussy")


@sus_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="button",
    description="This command does nothing... or does it?",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_sus_button(ctx: lightbulb.Context) -> None:
    view = SussyButton(timeout=60)
    message = await ctx.respond("sus linky...", components=view.build())
    view.start(await message.message())
    await view.wait()
    await ctx.respond("The button timed out, guess you were too slow!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sus_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sus_plugin)