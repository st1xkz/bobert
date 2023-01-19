import random

import hikari
import lightbulb

from bobert.core.stuff.langs import langs

greetings = lightbulb.Plugin("greetings")


@greetings.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    before = event.old_member
    after = event.member
    role = 1049570936376012862
    lg = random.choice(langs)

    if role in [r.id for r in after.get_roles()] and role not in [
        r.id for r in before.get_roles()
    ]:
        await greetings.bot.rest.create_message(
            993567969839960135,
            f"You made it {after.mention}! Welcome to **{event.member.get_guild().name}**, enjoy your stay 💚",
            user_mentions=True,
        )
        await after.send(
            "https://cdn.discordapp.com/attachments/848015340381274173/920115834460971058/welcome_banner.png"
        )
        await after.send(
            f"{lg} {after.mention}! You are now verified!\n\n"
            "To get started, please introduce yourself in <#794736957283893288> and get your <#800435987951124481>. You’re not required to, however, we highly recommend you do, that way you encourage others to do it.\n\n"
            "For a refresher of the rules, visit <#785551273734176828>. You can find more information in <#848015340381274173> or <#809215806323163136> if you're interested in learning more about what this server has to offer or is about.\n\n"
            "For more serious matters, such as someone who is struggling with mental health issues, contemplating suicide, or any other serious and/or related subject, we strongly advise you to post in <#1020363287281537104> for peer support or to look at <#796573173905752074> for a list of voice and chat/text hotline services as well as the 'Resources' section in <#809215806323163136>, where you can read more about related topics. 🌿"
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings)
