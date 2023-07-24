import asyncio

import hikari
import lightbulb

bump = lightbulb.Plugin("bump")


@bump.listener(hikari.MessageCreateEvent)
async def bump_reminder(event: hikari.MessageCreateEvent) -> None:
    if (
        event.author_id == 302050872383242240
        and "Bump done!" in event.message.embeds[0].description
    ):
        await event.message.respond(
            f"{event.message.interaction.user.mention} thanks for bumping the server! You'll be reminded in 2 hours!"
        )
        await asyncio.sleep(7200)

        embed = hikari.Embed(
            title="Bump time!",
            description="⌛ Bump our server by using `/bump` to make it bigger!",
            color=0xA3785D,
        )
        await bump.bot.rest.create_message(
            event.channel_id,
            content="<@&1062454520086548550>",
            embed=embed,
            role_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(bump)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(bump)
