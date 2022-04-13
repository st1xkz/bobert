from __future__ import annotations

import hikari
import lightbulb

import io
import asyncio
from datetime import datetime


image_plugin = lightbulb.Plugin("images")


ANIMALS = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Koala": "🐨",
    "Bird": "🐦",
}

@image_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="animalfact", aliases=["fact", "af"], description="Displays a fact + picture of a cute animal :3", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu(
            "animal_select"
        )
        .set_placeholder(
            "Pick an animal"
        )
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
        await msg.edit(
            "The menu timed out :c",
            components=[]
        )
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
                    f"Here's a {animal} fact for you! :3",
                    embed=embed,
                    components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c",
                    components=[]
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

@image_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="animal", aliases=["al"], description="Displays a picture of a cute animal :3", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def animal1_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu(
            "animal_select"
        )
        .set_placeholder(
            "Pick an animal"
        )
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
        await msg.edit(
            "The menu timed out :c",
            components=[]
        )
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
                    f"Here's a cute {animal} for you! :3",
                    embed=embed,
                    components=[]
                )
            else:
                await msg.edit(
                    f"API returned a `{res.status}` status :c",
                    components=[]
                )


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

my_items = {
    "pixelate": "https://some-random-api.ml/canvas/pixelate?avatar=$avatar",
    "blur": "https://some-random-api.ml/canvas/blur?avatar=$avatar",
    "stupid": "https://some-random-api.ml/canvas/its-so-stupid?avatar=$avatar&dog=im-stupid",
    "simp": "https://some-random-api.ml/canvas/simpcard?avatar=$avatar",
    "horny": "https://some-random-api.ml/canvas/horny?avatar=$avatar",
    "lolice": "https://some-random-api.ml/canvas/lolice?avatar=$avatar",
    "lgbtq+": "https://some-random-api.ml/canvas/lgbt?avatar=$avatar",
    "trans": "https://some-random-api.ml/canvas/transgender?avatar=$avatar"
}

@image_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="canvas", description="Displays a picture of the canvas you chose :3", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def canvas_command(ctx: lightbulb.Context) -> None | lightbulb.ResponseProxy:
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
                and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
            )
    except asyncio.TimeoutError:
        await msg.edit(
            "The menu timed out :c",
            components=[]
        )
    else:
        misc = event.interaction.values[0]
        url = my_items.get(misc).replace("$avatar", ctx.author.avatar_url.__str__())
        embed = hikari.Embed(color=0x000100, timestamp=datetime.now().astimezone())
        embed.set_image(url)
        
        misc = misc.replace("_", " ")
        
        await msg.edit(
            f"Here's your canvas! :3",
            embed=embed,
            components=[]
        )
        
"""
OVERLAYS = {
    "Glass": "🪟",
    "Wasted": "⚰️",
    "Mission Passed": "⭐",
    "Jail": "🧑‍⚖️",
    "Comrade": "🪖",
    "Triggered": "💢",
}

my_items = {
    "glass": "",
    "wasted": "",
    "mission passed": "",
    "jail": "",
    "comrade": "",
    "triggered": ""
}

@image_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(name="overlay", aliases=["ol"], description="Displays an overlay on your avatar :3", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def overlay_command(ctx: lightbulb.Context) -> None:
    select_menu = (
        ctx.bot.rest.build_action_row()
        .add_select_menu("overlay_select")
        .set_placeholder("Pick an overlay")
    )

    for name, emoji in OVERLAYS.items():
        select_menu.add_option(
            name,  # the label, which users see
            name.lower().replace(" ", "_"),  # the value, which is used by us later
        ).set_emoji(emoji).add_to_menu()

    resp = await ctx.respond(
        "Pick an overlay from the dropdown!",
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
        await msg.edit(
            "The menu timed out :c",
            components=[]
        )
    else:
        overlay = event.interaction.values[0]
        url = 
        embed = hikari.Embed(color=0x000100, timestamp=datetime.now().astimezone())
        embed.set_image(url)
                        
        overlay = overlay.replace("_", " ")

        await msg.edit(
            f"Here's your {overlay} overlay! :3",
            embed=embed,
            components=[]
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
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
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
    bot.add_plugin(image_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(image_plugin)