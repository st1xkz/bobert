import asyncio
import random
from datetime import datetime

import hikari
import lightbulb
import miru

confess = lightbulb.Plugin("confess")


# Main server channel IDs
LOGS_CH = 806649188146348043
CONFESS_CH = 806649868314869760
CONFESSION_CH = 806649874379964487


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
        await ctx.respond(
            f"Your confession has been sent to the <#{CONFESSION_CH}> channel!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        text = list(ctx.values.values())[0]
        user = ctx.user
        msg = await confess.bot.rest.create_message(
            CONFESSION_CH,
            embed=hikari.Embed(
                title="Confession", description=text, color=random.randint(0, 0xFFFFFF)
            ).set_footer(text="All confessions are anonymous."),
        )

        # Ensure that the context is from a guild and the member exists
        guild = ctx.get_guild()
        if guild is None:
            await ctx.respond("Guild not found.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        member = guild.get_member(user.id)
        if member is None:
            await ctx.respond(
                "Member not found in the guild.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        # Send to logs channel
        embed = (
            hikari.Embed(
                description=f"**Message sent from confess button** \n{text}",
                color=0xFF4040,
            )
            .set_author(
                name=f"{member.display_name} ({ctx.author})",
                icon=user.display_avatar_url if user else None,
            )
            .set_footer(text=f"UID: {ctx.user.id} | MID: {msg.id}")
        )
        await confess.bot.rest.create_message(LOGS_CH, embed=embed)


class ConfessButton(miru.Button):
    async def callback(self, ctx: miru.ViewContext) -> None:
        await ctx.respond_with_modal(Confess())
        ctx.view.stop()


@confess.command
@lightbulb.add_cooldown(300, 1, lightbulb.UserBucket)
@lightbulb.command(
    name="confess",
    description="Make a confession using buttons and modals",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def confess_cmd(ctx: lightbulb.Context) -> None:
    view = miru.View()
    view.add_item(ConfessButton(label="Make confession"))

    await ctx.respond(
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
    ctx.bot.d.miru.start_view(view)


@confess.listener(hikari.GuildMessageCreateEvent)
async def on_message(event: hikari.GuildMessageCreateEvent) -> None:
    message = event.message
    author = event.member

    if message.author.is_bot:
        return
    if message.channel_id == CONFESS_CH:
        # Send to confessions channel
        embed = hikari.Embed(
            title="Confession",
            description=f"{message.content}",
            color=random.randint(0, 0xFFFFFF),
        ).set_footer(text="All confessions are anonymous.")
        await confess.bot.rest.create_message(CONFESSION_CH, embed=embed)

        if author is not None:
            # Send to logs channel
            embed = (
                hikari.Embed(
                    description=f"**Message deleted in <#{CONFESS_CH}>** \n{message.content}",
                    color=0xFF4040,
                )
                .set_author(
                    name=f"{author.display_name} ({str(author)})",
                    icon=author.display_avatar_url,
                )
                .set_footer(text=f"UID: {author.id} | MID: {message.id}")
            )
            await confess.bot.rest.create_message(LOGS_CH, embed=embed)

        # Delete message from confess channel
        await message.delete()

        # Send message for confirmation
        msg = await confess.bot.rest.create_message(
            CONFESS_CH,
            embed=(
                hikari.Embed(
                    title="Success",
                    description=f"I've received your confession and sent it to the <#{CONFESSION_CH}> channel!",
                ).set_footer(text="Confessions")
            ),
        )
        await asyncio.sleep(1)
        await msg.delete()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess)
