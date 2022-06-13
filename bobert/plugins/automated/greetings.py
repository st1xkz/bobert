import hikari
import lightbulb

greetings_plugin = lightbulb.Plugin("greetings")

"""
@greetings_plugin.listener(hikari.MemberUpdateEvent)
async def on_member_join_update(event: hikari.MemberUpdateEvent) -> None:
    before = event.old_member
    after = event.member
    role = # get the role id
    if role in after.get_roles() and not in before.get_roles():
        await ctx.respond(f"You made it {after.mention}! Welcome to **{event.guild.name}**, enjoy your stay 💚")
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings_plugin)
