import hikari
import lightbulb

greetings_plugin = lightbulb.Plugin("greetings")


@greetings_plugin.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    with open("users.txt", "w+") as txt:
        str(event.member.id)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings_plugin)
