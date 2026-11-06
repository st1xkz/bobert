import hikari
import lightbulb

welcome = lightbulb.Plugin("welcome")

@welcome.listener(hikari.MemberUpdateEvent)
async def on_member_update(event: hikari.MemberUpdateEvent) -> None:
    member = event.member
    old_member = event.old_member
    role_id = 816858066330320897

    if old_member is None:
        return

    # Check whether the Members role was just added
    if (
        role_id in member.role_ids
        and role_id not in old_member.role_ids
    ):
        await welcome.bot.rest.create_message(
            781422576660250637,
            f"You made it, {member.mention}! Welcome to **Sage**, enjoy your stay 💚",
            user_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(welcome)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(welcome)
