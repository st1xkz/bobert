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
        self.add_item(miru.TextInput(label="Your confession here", style=hikari.TextInputStyle.PARAGRAPH, required=True))

    async def callback(self, ctx: miru.ModalContext) -> None:
        text = list(ctx.values.values())[0]
        await confess_plugin.bot.create_message(989713715203043378, text)


class ConfessButton(miru.Button):
    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(Confess())


@confess_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="confess",
    description="Make a confession using buttons",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_confess(ctx: lightbulb.Context) -> None:
    view = miru.View()
    view.add_item(ConfessButton(label="Make a confession"))
    res = await ctx.respond("Click here to make a confession!", components=view.build(), flags=hikari.MessageFlag.EPHEMERAL)
    msg = await res.message()
    await view.start(msg)
    await msg.delete()


@confess_plugin.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent) -> None:
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
        await confess_plugin.bot.rest.create_message(989713715203043378, embed)

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
            .set_footer(text=f"Author:  {author.id} | Message: {message.id}")
        )
        await confess_plugin.bot.rest.create_message(989715080918745148, embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess_plugin)
