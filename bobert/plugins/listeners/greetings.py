import hikari
import lightbulb

greetings_plugin = lightbulb.Plugin("greetings")


@greetings_plugin.listener(hikari.MemberUpdateEvent)
async def on_member_join_update(event: hikari.MemberUpdateEvent) -> None:
    with open("bobert/db/users.json", "w+") as j:
        j.write({str(event.member.id)})
"""
    before = event.old_member
    after = event.member
    role = 986449519615025202
    if role in [r.id for r in after.get_roles()] and role not in [
        r.id for r in before.get_roles()
    ]:
        await greetings_plugin.bot.rest.create_message(
            900466082618425365,
            f"You made it {after.mention}! Welcome to **{event.member.get_guild().name}**, enjoy your stay 💚",
            user_mentions=True,
        )
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings_plugin)
