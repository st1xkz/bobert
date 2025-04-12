import hikari
import lightbulb

welcome = lightbulb.Plugin("welcome")


@welcome.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    member = event.member
    role_id = 816858066330320897

    if (
        member.guild_flags & hikari.GuildMemberFlags.COMPLETED_ONBOARDING
        and role_id in member.role_ids
    ):
        await welcome.bot.rest.create_message(
            781422576660250637,  # Main server channel ID
            f"You made it, {member.mention}! Welcome to **Sage**, enjoy your stay 💚",
            user_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(welcome)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(welcome)
