import hikari
import lightbulb

from bobert.core.stuff import login_generator, random_common_word, random_dm
from bobert.core.stuff import text_to_owo, sites, to_ascii

import json
import random
import asyncio
from datetime import datetime
from random import randint


fun_plugin = lightbulb.Plugin("fun")


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="chucknorris", aliases=["chuck"], description="Chuck Norris Jokes.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def chucknorris_command(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://api.chucknorris.io/jokes/random"
    ) as resp:
        data = await resp.json()
    joke = data["value"]
    icon = data["icon_url"]
    
    embed = hikari.Embed(
        description=joke,
        color=0x8B0000
    )
    embed.set_thumbnail(icon)
    await ctx.respond(embed)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "what do you want to pay respect to?", type=str, required=False, modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.command(name="f", description="Press F to pay respect.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def f_command(ctx: lightbulb.Context) -> None:
    hearts = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤍', '🤎']
    reason = f"for **{ctx.options.text}** " if ctx.options.text else ""
    await ctx.respond(
        f"**{ctx.author.username}** has paid their respect {reason}{random.choice(hearts)}"
    )


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("digits", "The number of digits to send", type=int)
@lightbulb.command(name="randomnumber", aliases=["rn"], description="Generates a random number with the specified length of digits")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def number_command(ctx: lightbulb.Context) -> None:
    number = ""
    
    for i in range(ctx.options.digits):
        number += str(random.randint(0, 9))
    await ctx.respond(number)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to be sent")
@lightbulb.command(name="reverse", aliases=["rev"], description="Reverses text")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def rev_command(ctx: lightbulb.Context) -> None:
    t_rev = ctx.options.text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
    await ctx.respond(t_rev)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to be sent", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("user_id", "The user's ID", required=False)
@lightbulb.command(name="dm", description="DMs given user through the bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dm_command(ctx: lightbulb.Context) -> None:
    user = ctx.bot.cache.get_user(ctx.options.user_id)
    await user.send(ctx.options.text)
    await ctx.respond(
        f"Your message has been sent to the specified user! ({user.username})"
    ) # finish this command


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to be sent", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="dmall", description="DMs all users in the server through the bot")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dmall_command(ctx: lightbulb.Context) -> None:
    if ctx.options.text != None:
        for member in ctx.get_guild().get_members().keys():
            if member == ctx.bot.get_me().id: continue
            await ctx.get_guild().get_member(member).send(ctx.options.text)
            
        await ctx.respond(
            "Your message has been sent to everyone!"
        ) # finish this command


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to send", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.option("member", "The Discord member", hikari.User)
@lightbulb.command(name="sudo", description="Puts words into other peoples mouth's")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def sudo_command(ctx: lightbulb.Context) -> None:
    for k in await ctx.bot.rest.fetch_guild_webhooks(ctx.guild_id):
        if k.author == ctx.author:
            await k.delete()
    webhook = await ctx.bot.rest.create_webhook(name=f"{ctx.options.member}", channel=ctx.channel_id)
        
    await webhook.execute(ctx.options.text, username=ctx.options.member.username, avatar_url=ctx.options.member.avatar_url or ctx.options.member.default_avatar_url, mentions_everyone=False, user_mentions=False, role_mentions=False)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to send", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="ascii", description="Turns text to ascii")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ascii_command(ctx: lightbulb.Context) -> None:
    ascii_text = to_ascii(ctx.options.text)
    if len(ascii_text) < 2000:
        ascii_text = to_ascii(ctx.options.text, True)
        if len(ascii_text) > 2000:
            await ctx.respond(
                "Error: Input is too long",
                delete_after=10
            )
            return
        await ctx.respond(ascii_text)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="useless", aliases=["uls"], description="Gives you a random/useless website")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def useless_command(ctx: lightbulb.Context) -> None: 
        randomsite = random.choice(sites)  
        embed = hikari.Embed(
            title="Here's your useless website:",
            description=f"🌐 {randomsite}",
            color=randint(0, 0xffffff)
        )
        await ctx.respond(embed)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "The text to send", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="owo", description="Turns text to owo (e.g. hewwo)")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def owo_command(ctx: lightbulb.Context) -> None:
    await ctx.respond(text_to_owo(ctx.options.text))


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="advice", description="Don't be afraid to ask for advice!", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def advice_command(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        f"https://api.adviceslip.com/advice"
    ) as resp:
        data = json.loads(await resp.read())
    adv = data["slip"]["advice"]
    await ctx.respond(adv)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="coinflip", aliases=["cf"], description="Flip a coin!")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cf_command(ctx: lightbulb.Context) -> None:
    choices = ["Heads!", "Tails!"]
    rancoin = random.choice(choices)
    await ctx.respond(rancoin)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User, required=False)
@lightbulb.command(name="cool", description="Checks how cool someone is")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cool_command(ctx: lightbulb.Context) -> None:
    member = ctx.author

    if ctx.options.member:
        embed = hikari.Embed(
            title="Cool Rate",
            description=f"{ctx.options.member.mention}, you are **{random.randrange(101)}%** cool! 😎"
        )
        await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title="Cool Rate",
            description=f"{member.mention}, you are **{random.randrange(101)}%** cool! 😎"
        )
        await ctx.respond(embed)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User, required=False)
@lightbulb.command(name="gay", description="Checks how gay someone is")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def gay_command(ctx: lightbulb.Context) -> None:
    member = ctx.author

    if ctx.options.member:
        embed = hikari.Embed(
            title="Gay Rate",
            description=f"{ctx.options.member.mention}, you are **{random.randrange(101)}%** gay! 🏳️‍🌈"
        )
        await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title="Gay Rate",
            description=f"{member.mention}, you are **{random.randrange(101)}%** gay! 🏳️‍🌈"
        )
        await ctx.respond(embed)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User, required=False)
@lightbulb.command(name="pp", description="Checks the size of someone's pp")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def pp_command(ctx: lightbulb.Context) -> None:
    ctx.options.member = ctx.author
    pp = ['8D', '8=D', '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D', '8=========D', '8==========D', '8===========D', '8============D', '8=============D']

    if ctx.options.member:
        embed = hikari.Embed(
            title=f"{ctx.options.member.mention}'s pp:",
            description=f"{random.choice(pp)}"
        )
        await ctx.respond(embed)
    else:
        embed = hikari.Embed(
            title="Your pp:",
            description=f"{random.choice(pp)}"
        )
        await ctx.respond(embed)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("question", "The question to be asked")
@lightbulb.command(name="8ball", description="Wisdom. Ask a question and the bot will give you an answer")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def _8ball(ctx: lightbulb.Context) -> None:
    responses = ['It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes – definitely.', 'You may rely on it.', 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.', 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.']
    await ctx.respond(
        f"{random.choice(responses)}"
    )


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("bonus", "A fixed number to add to the total roll", int, default=0)
@lightbulb.option("sides", "The number of sides each die will have", int, default=6)
@lightbulb.option("number", "The number of dice to roll", int)
@lightbulb.command(name="dice", description="Roll one or more dice")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def dice_command(ctx: lightbulb.Context) -> None:
    number = ctx.options.number
    sides = ctx.options.sides
    bonus = ctx.options.bonus

    if number > 25:
        await ctx.respond(
            "No more than 25 dice can be rolled at once.",
            delete_after=10
        )
        return

    if sides > 100:
        await ctx.respond(
            "The dice cannot have more than 100 sides.",
            delete_after=10
        )
        return

    rolls = [random.randint(1, sides) for _ in range(number)]

    await ctx.respond(
        " + ".join(f"{r}" for r in rolls)
        + (f" + {bonus} (bonus)" if bonus else "")
        + f" = **{sum(rolls) + bonus:,}**"
    )


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("user", "User to greet", hikari.User)
@lightbulb.command(name="greet", description="Greets the specified user")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def greet_command(ctx: lightbulb.Context) -> None:
    await ctx.respond(
        f"Hello {ctx.options.user.mention}!"
    )


@fun_plugin.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("text", "Text to repeat", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.command(name="echo", aliases=["say"], description="Repeats the user's input")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def echo_command(ctx: lightbulb.Context) -> None:
    await ctx.respond(ctx.options.text)


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option("member", "The Discord member", hikari.User)
@lightbulb.command(name="hack", description="\"hacks\" a member")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def hack_command(ctx: lightbulb.Context) -> None:
    ran_sleep = random.uniform(1.75, 2.25)
    email, password = login_generator(ctx.options.member.username)
    friends = random.randint(0, 1)
    _dm = random_dm()
    common_word = random_common_word()
    member_disc = str(ctx.options.member.discriminator)
    random_port = random.randint(1123, 8686)
    random_subnet = random.choice(('192.168.0.', '192.168.1.', '192.168.2.'))
    random_ip = random.randint(0, 254)
    
    msg = await ctx.respond(
        f"Hacking {ctx.options.member.username} now..."
    )
    
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Finding discord login... (2fa bypassed)"
    )
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Found login info...\n**Email**: `{email}`\n**Password**: `{password}`"
    )
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Fetching DMs with closest friends (if there are any friends at all)..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)

    if friends == 0:
        await msg.edit(
            content=f"No DMs found."
        )
    else:
        await msg.edit(
            content=f"DMs found...\n**Last DM**: \"{_dm}\""
        )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Finding most common word..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Most common word = \"{common_word}\""
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Injecting trojan virus into member discriminator: #{member_disc}"
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Setting up Epic Store account..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Hacking Epic Store account..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Finding IP address..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"IP Address Found!\n**IP address**: {random_subnet}{random_ip}:{random_port}"
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Reporting account to Discord for breaking TOS..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Hacking medical records..."
    )
    
    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content="Selling member\'s data to the Government..."
    )

    async with ctx.get_channel().trigger_typing():
        await asyncio.sleep(ran_sleep)
    await msg.edit(
        content=f"Finished hacking {ctx.options.member.username}!"
    )
    
    await ctx.respond(
        "The *totally* real and **dangerous** hack is complete."
    )


@fun_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="meme", description="Displays a random meme from Reddit")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def meme_command(ctx: lightbulb.Context) -> None:
    async with ctx.bot.d.aio_session.get(
        "https://meme-api.herokuapp.com/gimme"
    ) as response:
        res = await response.json()

        if response.ok and res["nsfw"] != True:
            link = res["postLink"]
            title = res["title"]
            img_url = res["url"]

            embed = hikari.Embed(
                title=title,
                color=randint(0, 0xffffff),
                timestamp=datetime.now().astimezone(),
                url=link
            )
            embed.set_author(
                name=f"{ctx.author.username}#{ctx.author.discriminator}",
                icon=ctx.author.avatar_url
            )
            embed.set_image(img_url)
            embed.set_footer(
                text="Here is your meme!"
            )

            await ctx.respond(embed)

        else:
            await ctx.respond(
                "Could not fetch a meme :c", flags=hikari.MessageFlag.EPHEMERAL
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(fun_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(fun_plugin)