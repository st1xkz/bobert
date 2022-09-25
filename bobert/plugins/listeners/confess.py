import asyncio
import random
from datetime import datetime

import hikari
import lightbulb
import miru

confess_plugin = lightbulb.Plugin("confess")


class Confess(miru.Modal):
    def __init__(self) -> None:
        super().__init__("Make a confession")
        self.add_item(
            miru.TextInput(
                label="Confessions",
                placeholder="Type your confession here",
                style=hikari.TextInputStyle.PARAGRAPH,
                required=True,
            )
        )

    async def callback(self, ctx: miru.ModalContext) -> None:
        text = list(ctx.values.values())[0]
        user = ctx.user
        msg = await confess_plugin.bot.rest.create_message(
            989713715203043378,
            embed=hikari.Embed(
                title="Confession", description=text, color=random.randint(0, 0xFFFFFF)
            ).set_footer(text="All confessions are anonymous."),
        )

        # send to logs channel
        embed = (
            hikari.Embed(
                description=f"**Message sent from confess button** \n{text}",
                color=0xFF4040,
            )
            .set_author(
                name=f"{ctx.get_guild().get_member(user.id).nickname} ({ctx.user})",
                icon=ctx.user.avatar_url or ctx.user.default_avatar_url,
            )
            .set_footer(text=f"Author: {ctx.user.id} | Message: {msg.id}")
        )
        await confess_plugin.bot.rest.create_message(989715080918745148, embed=embed)


class ConfessButton(miru.Button):
    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(Confess())
        ctx.view.stop()


@confess_plugin.command
@lightbulb.add_cooldown(500, 1, lightbulb.UserBucket)
@lightbulb.command(
    name="confess",
    description="Make a confession using buttons and modals",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_confess(ctx: lightbulb.Context) -> None:
    view = miru.View()
    view.add_item(ConfessButton(label="Make confession"))

    proxy = await ctx.respond(
        embed=hikari.Embed(
            description="""⚠️ **Do not send random, pointless messages**

⚠️ **Do not harass anyone**

⚠️ **Add content warnings, trigger warnings, or spoil anything that could be potentially harmful or triggering to somebody. If your post requires them and does not contain them, your post will be deleted until it is added.**

""",
            color=0x2F3136,
            timestamp=datetime.now().astimezone(),
        ).set_footer(text="Confessions"),
        components=view.build(),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
    view.start(await proxy.message())
    await view.wait()
    await ctx.respond(
        "Your confession has been sent to the <#989713715203043378> channel!",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@confess_plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    message = event.message
    author = event.member

    if message.author.is_bot:
        return
    if message.channel_id == 989713657078382692:
        await message.delete()

        # delete message from confess channel and send message for confirmation
        msg = await confess_plugin.bot.rest.create_message(
            989713657078382692,
            embed=(
                hikari.Embed(
                    title="Success",
                    description="I've received your confession and sent it to the <#989713657078382692> channel!",
                    color=0x2F3136,
                ).set_footer(text="Confessions")
            ),
        )
        await asyncio.sleep(1)
        await msg.delete()

        # send to confessions channel
        embed = hikari.Embed(
            title="Confession",
            description=f"{message.content}",
            color=random.randint(0, 0xFFFFFF),
        ).set_footer(text="All confessions are anonymous.")
        await confess_plugin.bot.rest.create_message(989713715203043378, embed=embed)

        # send to logs channel
        embed = (
            hikari.Embed(
                description=f"**Message deleted in <#989713657078382692>** \n{message.content}",
                color=0xFF4040,
            )
            .set_author(
                name=f"{author.nickname} ({str(author)})",
                icon=author.avatar_url or author.default_avatar_url,
            )
            .set_footer(text=f"Author: {author.id} | Message: {message.id}")
        )
        await confess_plugin.bot.rest.create_message(989715080918745148, embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess_plugin)
