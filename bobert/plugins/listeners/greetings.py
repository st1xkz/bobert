import hikari
import lightbulb

greetings_plugin = lightbulb.Plugin("greetings")


@greetings_plugin.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    before = event.old_member
    after = event.member
    role = 993695690578464778

    with open("bobert/db/users.json", "w+") as j:
        j.write({str(event.member.id)})
        
        if role in [r.id for r in after.get_roles()] and role not in [
            r.id for r in before.get_roles()
        ]:
            await greetings_plugin.bot.rest.create_message(
                993567995936915536,
                f"You made it {after.mention}! Welcome to **{event.member.get_guild().name}**, enjoy your stay 💚",
                user_mentions=True,
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings_plugin)
