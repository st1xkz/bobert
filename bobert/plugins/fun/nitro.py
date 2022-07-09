import hikari
import lightbulb
import miru


class SussyButton(miru.View):
    @miru.button(
        label="Claim",
        emoji=hikari.Emoji.parse("<:nitro:994361557377101924>"),
        style=hikari.ButtonStyle.PRIMARY,
    )
    async def sussy_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond(
            "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


nitro_plugin = lightbulb.Plugin("nitro")


@nitro_plugin.command
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
            description=f"<:nitro:994361557377101924> **{ctx.author.mention} generated a nitro link!**",
            color=0xB674EF,
        ).set_image(
            "https://cdn.discordapp.com/attachments/900458968588120154/991825003920244916/Discord-Nitro-800x479.png"
        ),
        components=view.build(),
    )
    view.start(await message.message())
    await view.wait()
    embed = hikari.Embed(
        description=f"**Looks like {ctx.author.mention} didn't want it or they went AFK**",
        color=0xB674EF,
    ).set_image(
        "https://cdn.discordapp.com/attachments/900458968588120154/991825003920244916/Discord-Nitro-800x479.png"
    )
    await message.edit(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(nitro_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(nitro_plugin)
