import asyncio
import random

import hikari
import lightbulb

from bobert.core.stuff import login_generator, random_common_word, random_dm

hack = lightbulb.Plugin("hack")


@hack.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="@member/id",
    description="the member you want to hack",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="hack",
    description='"Hacks" a member',
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _hack(ctx: lightbulb.Context, member: hikari.Member) -> None:
    ran_sleep = random.uniform(1.75, 2.25)
    email, password = login_generator(member.username)
    friends = random.randint(0, 1)
    _dm = random_dm()
    common_word = random_common_word()
    member_disc = str(member.discriminator)
    random_port = random.randint(1123, 8686)

    starting_msg = f"hacking member: {member.username}"
    msg = await ctx.respond(
        f"```py\n{starting_msg}```", reply=False, mentions_reply=False
    )
    new_msg_list = f"hacking member: {member.username}"
    f = random.randint(100, 900)
    d = random.randint(10, 90)
    ip = f"192.168.{f}.{d}"

    msg_loop = [
        "\nexec hack",
        ".",
        ".",
        ".",
        "\nfinding discord login",
        ".",
        ".",
        ".",
        " (2fa bypassed)",
        f"\nfound login info",
        ".",
        ".",
        ".",
        f"\n    Email: ",
        f"{email}",
        f"\n    Password: ",
        f"{password}",
        "\nfetching DMs with closest friends (if there are any friends at all)",
        ".",
        ".",
        ".",
        f"\n{friends}"
        if friends == "No DMs found."
        else ("\nDMs found..." f"\n    last DM: {_dm}"),
        "\nfinding most common word",
        ".",
        ".",
        ".",
        f'\nmost common word = "{common_word}"',
        f"\ninjecting trojan virus into member discriminator: ",
        f"#{member_disc}",
        "\nsetting up Epic Store account",
        ".",
        ".",
        ".",
        "\nhacking Epic Store account",
        ".",
        ".",
        ".",
        "\nfinding IP address",
        ".",
        ".",
        ".",
        f"\nIP Address Found!",
        "\n    IP address: ",
        f"{ip}:{random_port}",
        "\nreporting account to Discord for breaking TOS",
        ".",
        ".",
        ".",
        "\nhacking medical records",
        ".",
        ".",
        ".",
        "\nselling member's data to the Government",
        ".",
        ".",
        ".",
        f"\n{member.display_name} has been successfully hacked.",
    ]
    for k in msg_loop:
        for end in (".", "-", ":"):
            if k.endswith(end):
                new_msg_list += f"{k}"
                break
            else:
                new_msg_list += k
                break

        await msg.edit(content=f"```py\n{new_msg_list}```")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(hack)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(hack)
