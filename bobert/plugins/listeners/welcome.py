import hikari
import lightbulb

welcome = lightbulb.Plugin("welcome")


@welcome.listener(hikari.MemberUpdateEvent)
async def on_member_join_update(event: hikari.MemberUpdateEvent) -> None:
    before = event.old_member
    after = event.member
    role = 816858066330320897

    if (
        after is not None
        and before is not None
        and role in [r.id for r in after.get_roles()]
        and role not in [r.id for r in before.get_roles()]
    ):
        await welcome.bot.rest.create_message(
            781422576660250637,  # Main server channel ID
            f"You made it, {after.mention}! Welcome to **Sage**, enjoy your stay 💚",
            user_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(welcome)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(welcome)
