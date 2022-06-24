import asyncio
import random

import hikari
import lightbulb

confess_plugin = lightbulb.Plugin("confess")


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
