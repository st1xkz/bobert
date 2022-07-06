import asyncio
import random

import hikari
import lightbulb

from bobert.core.stuff import login_generator, random_common_word, random_dm

hack_plugin = lightbulb.Plugin("hack")


@hack_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="hack",
    description='"hacks" a member',
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_hack(ctx: lightbulb.Context) -> None:
    ran_sleep = random.uniform(1.75, 2.25)
    email, password = login_generator(ctx.options.member.username)
    friends = random.randint(0, 1)
    _dm = random_dm()
    common_word = random_common_word()
    member_disc = str(ctx.options.member.discriminator)
    random_port = random.randint(1123, 8686)

    starting_msg = f"Hacking member: {ctx.options.member.username}"
    msg = await ctx.respond(f"```py\n{starting_msg}```", reply=True)
    new_msg_list = f"Hacking member: {ctx.options.member.username}"
    f = random.randint(100, 900)
    d = random.randint(10, 90)
    ip = f"192.168.{f}.{d}"

    if friends == 0:
        await msg.edit(content=f"No DMs found.")
    else:
        await msg.edit(content=f"DMs found...\n" f'**Last DM**: "{_dm}"')

    msg_loop = [
        "\nExecuting hack.",
        ".",
        ".",
        "\nFinding discord login... (2fa bypassed)",
        f"\nFound login info...\n    Email: {email}\n    Password: {password}",
        "\nFetching DMs with closest friends (if there are any friends at all)...",
        f"\n{friends}",
        "\nFinding most common word.",
        ".",
        ".",
        f'\nMost common word = "{common_word}"',
        f"\nInjecting trojan virus into member discriminator: #{member_disc}",
        "\nSetting up Epic Store account.",
        ".",
        ".",
        "\nHacking Epic Store account.",
        ".",
        ".",
        "\nFinding IP address.",
        ".",
        ".",
        f"\nIP Address Found!\n    IP address: {ip}:{random_port}",
        "\nReporting account to Discord for breaking TOS...",
        "\nHacking medical records...",
        "\nSelling member's data to the Government...",
        f"\n{ctx.options.member.nickname} has been successfully hacked.",
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
    bot.add_plugin(hack_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(hack_plugin)
