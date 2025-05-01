import hikari
import lightbulb

welcome = lightbulb.Plugin("welcome")

"""
@welcome.listener(hikari.MemberUpdateEvent)
async def on_member_approved(event: hikari.MemberUpdateEvent) -> None:
    member = event.member

    # verify the event is being triggered
    print(f"Member update received for {member.username} ({member.id})")

    if member.is_pending is False:
        await welcome.bot.rest.create_message(
            993567969839960135,
            f"You made it, {member.mention}! Welcome to **Sage**, enjoy your stay 💚",
            user_mentions=True,
        )
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(welcome)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(welcome)
