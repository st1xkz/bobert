import hikari
import lightbulb

import io
import asyncio
from datetime import datetime


plugin = lightbulb.Plugin("images")


ANIMALS = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Koala": "🐨",
    "Bird": "🐦",
}

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.command(name="animalfact", aliases=["fact", "af"], description="Displays a fact + picture of a cute animal :3")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in ANIMALS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown!",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=300,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(description=res["fact"], color=0x000100, timestamp=datetime.now().astimezone())
                embed.set_image(res["image"])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a {animal} fact for you! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c", components=[]
                )


ANIMALS1 = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Red Panda": "🐼",
    "Koala": "🐨",
    "Bird": "🐦",
}

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.command(name="animal", aliases=["al"], description="Displays a picture of a cute animal :3")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal1_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in ANIMALS1.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown!",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=300,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/img/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(color=0x000100, timestamp=datetime.now().astimezone())
                embed.set_image(res['link'])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a cute {animal} for you! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c", components=[]
                )


"""
CANVAS = {
    "Pixelate": "👾",
    "Blur": "🌫",
    "YouTube": "🖥️",
    "Tweet": "💬",
    "Stupid": "🗿",
    "Simp": "🥺",
    "Horny": "🤤",
    "Lolice": "🚓",
    "LGBTQ+": "🏳️‍🌈",
    "Trans": "🏳️‍⚧️"
}

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.command(name="canvas", description="Displays a picture of the canvas you chose :3")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def canvas_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("canvas_select")
        .set_placeholder("Pick a canvas")
    )

    for name, emoji in CANVAS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick a canvas from the dropdown!",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=300,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        misc = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/canvas/{misc}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(color=0x000100, timestamp=datetime.now().astimezone())
                embed.set_image(res["image"])

                misc = misc.replace("_", " ")

                await msg.edit(
                    f"Here's your canvas! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c", components=[]
                )
"""


"""
OVERLAYS = {
    "Glass": "🪟",
    "Wasted": "⚰️",
    "Mission Passed": "⭐",
    "Jail": "",
    "Comrade": "",
    "Triggered": "",
}

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.command(name="animal", aliases=["al"], description="Displays a picture of a cute animal :3")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal1_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in OVERLAYS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown!",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=300,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/img/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(color=0x000100, timestamp=datetime.now().astimezone())
                embed.set_image(res['link'])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a cute {animal} for you! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c", components=[]
                )
"""

"""
FILTERS = {
    "Greyscale": "🐶",
    "Invert": "🐱",
    "Invert Greyscale": "🐼",
    "Brightness": "🦊",
    "Threshold": "🐨",
    "Sepia": "🐦",
    "Blurple": "",
    "Color": ""
}

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.command(name="animalfact", aliases=["fact", "af"], description="Displays a fact + picture of a cute animal :3")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("animal_select")
        .set_placeholder("Pick an animal")
    )

    for name, emoji in FILTERS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an animal from the dropdown!",
        component=select_menu.add_to_container(),
    )
    msg = await resp.message()

    try:
        event = await ctx.bot.wait_for(
            hikari.InteractionCreateEvent,
            timeout=300,
            predicate=lambda e:
                isinstance(e.interaction, hikari.ComponentInteraction)
                and e.interaction.user.id == ctx.author.id
                and e.interaction.message.id == msg.id
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU
            )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        async with ctx.bot.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
                embed = hikari.Embed(description=res["fact"], color=0x000100, timestamp=datetime.now().astimezone())
                embed.set_image(res["image"])

                animal = animal.replace("_", " ")

                await msg.edit(
                    f"Here's a {animal} fact for you! :3", embed=embed, components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c", components=[]
                )
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)