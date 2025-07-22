import random

import hikari
import lightbulb

confess = lightbulb.Plugin("confess")


# Main server channel IDs
LOGS_CH = 806649188146348043
CONFESS_CH = 806649868314869760
CONFESSION_CH = 806649874379964487


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

        await message.delete()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(confess)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(confess)
