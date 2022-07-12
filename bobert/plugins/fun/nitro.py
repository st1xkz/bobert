import hikari
import lightbulb
import miru


class NitroButton(miru.View):
    @miru.button(
        label="Claim",
        emoji=hikari.Emoji.parse("<:nitro:994361557377101924>"),
        style=hikari.ButtonStyle.PRIMARY,
    )
    async def nitro_button(self, button: miru.Button, ctx: miru.Context) -> None:
        await ctx.respond(
            "https://cdn.discordapp.com/attachments/900458968588120154/986732631859265546/rickroll-roll.gif",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        ctx.view.stop()

        button.style = hikari.ButtonStyle.DANGER
        button.label = "Claimed!"
        button.disabled = True
        self.clear_items()
        self.add_item(button)
        await self.message.edit(
            embed=hikari.Embed(
                description=f"**{ctx.author.mention} claimed the nitro!**",
                color=0xB674EF,
            ).set_image(
                "https://cdn.discordapp.com/attachments/900458968588120154/991825003920244916/Discord-Nitro-800x479.png"
            ),
            components=self.build(),
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
    view = NitroButton()
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


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(nitro_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(nitro_plugin)
