import hikari
import lightbulb

from bobert.core.utils import helpers

suggestion = lightbulb.Plugin("suggestions")

SUGGESTION_CH = 794647761558437938


@suggestion.listener(hikari.GuildMessageCreateEvent)
async def on_suggestion_message(event: hikari.GuildMessageCreateEvent) -> None:
    message = event.message
    author = event.member

    if author is None:
        return

    color = (
        c[0]
        if (c := [r.color for r in helpers.sort_roles(author.get_roles()) if r.color])
        else None
    )

    if message.author.is_bot:
        return
    if message.channel_id == SUGGESTION_CH:
        await message.delete()

        suggestion_embed = await suggestion.bot.rest.create_message(
            SUGGESTION_CH,
            embed=hikari.Embed(
                title="💡 New Suggestion",
                description=message.content,
                color=color,
            ).set_footer(
                text=f"Suggested by {author.display_name}",
                icon=author.display_avatar_url,
            ),
        )

        # Add reactions to suggestion embed
        await suggestion_embed.add_reaction("✅")
        await suggestion_embed.add_reaction("❌")

        # Create thread for suggestion
        thread = await suggestion_embed.app.rest.create_message_thread(
            event.channel_id,
            suggestion_embed.id,
            "Reply to Suggestion",
        )

        assert isinstance(
            thread, hikari.GuildPublicThread
        ), "Expected a GuildPublicThread"


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(suggestion)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(suggestion)
