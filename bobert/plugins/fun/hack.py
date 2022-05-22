import hikari
import lightbulb

from bobert.core.stuff import login_generator, random_common_word, random_dm

import random
import asyncio


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
    random_subnet = random.choice(("192.168.0.", "192.168.1.", "192.168.2."))
    random_ip = random.randint(0, 254)

    msg = await ctx.respond(f"Hacking {ctx.options.member.username} now...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Finding discord login... (2fa bypassed)")
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Found login info...\n"
        f"**Email**: `{email}`\n**Password**: `{password}`"
    )
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Fetching DMs with closest friends (if there are any friends at all)..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)

    if friends == 0:
        await msg.edit(content=f"No DMs found.")
    else:
        await msg.edit(content=f"DMs found...\n" f'**Last DM**: "{_dm}"')

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Finding most common word...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content=f'Most common word = "{common_word}"')

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Injecting trojan virus into member discriminator: #{member_disc}"
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Setting up Epic Store account...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Hacking Epic Store account...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Finding IP address...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"IP Address Found!\n"
        f"**IP address**: {random_subnet}{random_ip}:{random_port}"
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Reporting account to Discord for breaking TOS...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Hacking medical records...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content="Selling member's data to the Government...")

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(content=f"Finished hacking {ctx.options.member.username}!")

    await ctx.respond("The *totally* real and **dangerous** hack is complete.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(hack_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(hack_plugin)
