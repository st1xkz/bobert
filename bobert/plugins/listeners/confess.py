import asyncio
import random
from datetime import datetime

import hikari
import lightbulb
import miru

confess = lightbulb.Plugin("confess")

logs_ch = 1049483581711458414
confess_ch = 1049483623377670174
confession_ch = 1049483645137727538


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
        msg = await confess.bot.rest.create_message(
            confess_ch,
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
        await confess.bot.rest.create_message(logs_ch, embed=embed)


class ConfessButton(miru.Button):
    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(Confess())
        ctx.view.stop()


@confess.command
@lightbulb.add_cooldown(500, 1, lightbulb.UserBucket)
@lightbulb.command(
    name="confess",
    description="Make a confession using buttons and modals",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _confess(ctx: lightbulb.Context) -> None:
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
    await view.start(await proxy.message())
    await view.wait()
    await ctx.respond(
        f"Your confession has been sent to the <#{confession_ch}> channel!",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@confess.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    message = event.message
    author = event.member

    if message.author.is_bot:
        return
    if message.channel_id == confess_ch:
        await message.delete()

        # delete message from confess channel and send message for confirmation
        msg = await confess.bot.rest.create_message(
            confess_ch,
            embed=(
                hikari.Embed(
                    title="Success",
                    description=f"I've received your confession and sent it to the <#{confession_ch}> channel!",
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
        await confess.bot.rest.create_message(confession_ch, embed=embed)

        # send to logs channel
        embed = (
            hikari.Embed(
                description=f"**Message deleted in <#{confess_ch}>** \n{message.content}",
                color=0xFF4040,
            )
            .set_author(
                name=f"{author.nickname} ({str(author)})",
                icon=author.avatar_url or author.default_avatar_url,
            )
            .set_footer(text=f"Author: {author.id} | Message: {message.id}")
        )
        await confess.bot.rest.create_message(logs_ch, embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess)
