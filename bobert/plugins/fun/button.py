import hikari
import lightbulb
import miru


class SussyButton(miru.View):
    @miru.button(
        label="Claim",
        emoji=hikari.Emoji.parse("<:Nitro:991822580241674291>"),
        style=hikari.ButtonStyle.PRIMARY,
    )
    async def sussy_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond(
            "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


sus_plugin = lightbulb.Plugin("sussy")


@sus_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="nitro",
    description="Free nitro links!",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_sus_button(ctx: lightbulb.Context) -> None:
    view = SussyButton(timeout=60)
    message = await ctx.respond(
        embed=hikari.Embed(
            description=f"<:Nitro:991822580241674291> {ctx.author} generated a nitro link!",
            color=0xB674EF,
        ).set_image(
            "https://cdn.discordapp.com/attachments/900458968588120154/991825003920244916/Discord-Nitro-800x479.png"
        ),
        components=view.build(),
    )
    view.start(await message.message())
    await view.wait()
    await ctx.respond("The button timed out, guess you were too slow!")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(sus_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(sus_plugin)
