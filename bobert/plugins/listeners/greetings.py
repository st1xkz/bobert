import hikari
import lightbulb

greetings_plugin = lightbulb.Plugin("greetings")


@greetings_plugin.listener(hikari.MemberUpdateEvent)
async def on_member_join_update(event: hikari.MemberUpdateEvent) -> None:
    print("kek")
    before = event.old_member
    after = event.member
    role = 986449519615025202
    if role in after.get_roles() and role not in before.get_roles():
        print(role)
        await greetings_plugin.bot.create_message(900466082618425365, f"You made it {after.mention}! Welcome to **{after.guild.name}**, enjoy your stay 💚")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings_plugin)
