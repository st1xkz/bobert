import hikari
import lightbulb

greetings = lightbulb.Plugin("greetings")

"""
TODO:
    - Add database for welcome message so bot won't send message whenever user gets member role again
    - Add verification welcome message to send to user's DM when they verify into the server
"""


@greetings.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    before = event.old_member
    after = event.member
    role = 993695690578464778

    if role in [r.id for r in after.get_roles()] and role not in [
        r.id for r in before.get_roles()
    ]:
        await greetings.bot.rest.create_message(
            993567995936915536,
            f"You made it {after.mention}! Welcome to **{event.member.get_guild().name}**, enjoy your stay 💚",
            user_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings)
