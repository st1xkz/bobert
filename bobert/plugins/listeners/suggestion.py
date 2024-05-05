import json

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

        try:
            with open("bobert/core/utils/db/json/suggestion_nums.json", "r") as file:
                data = json.load(file)
                suggestion_number = data.get("suggestion_numbers", 18)  # Start at 18
        except FileNotFoundError:
            suggestion_number = 18  # Defaults to 18 if file doesn't exist

        suggestion_embed = await suggestion.bot.rest.create_message(
            SUGGESTION_CH,
            embed=hikari.Embed(
                title=f"💡 Suggestion `#{suggestion_number}`",
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
        thread: hikari.GuildPublicThread = (
            await suggestion_embed.app.rest.create_message_thread(
                event.channel_id,
                suggestion_embed.id,
                f"Reply to Suggestion {suggestion_number}",
            )
        )

        # Increment suggestion number and update JSON file
        suggestion_number += 1
        with open("bobert/core/utils/json_db/suggestion_nums.json", "w") as file:
            json.dump({"suggestion_numbers": suggestion_number}, file)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(suggestion)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(suggestion)
