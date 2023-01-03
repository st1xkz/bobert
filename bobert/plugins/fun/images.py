from __future__ import annotations

import asyncio
from random import randint

import DuckDuck
import hikari
import lightbulb
from bobert.core.utils import constants as const

client = DuckDuck.Duck()
image = lightbulb.Plugin("images")


ANIMALS = {
    "Dog": "🐶",
    "Cat": "🐱",
    "Panda": "🐼",
    "Fox": "🦊",
    "Red Panda": "🐼",
    "Koala": "🐨",
    "Bird": "🐦",
    "Raccoon": "🦝",
    "Kangaroo": "🦘",
    "Duck": "🦆",
}


async def cmd_duck_duck() -> str:
    url = await client.fetch_random()
    return url


async def get_animal_image(animal: str):
    if animal == "duck":
        url = await cmd_duck_duck()
        res = {"image": url, "fact": "Sorry, no duck facts."}
    else:
        async with image.bot.d.aio_session.get(
            f"https://some-random-api.ml/animal/{animal}"
        ) as res:
            if res.ok:
                res = await res.json()
            else:
                raise BaseException("API didn't respond")

    return res


@image.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="animal-fact",
    description="Displays a fact along with a cute animal picture: 3",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def animal_fact(ctx: lightbulb.Context) -> None:
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

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
            predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.user.id == ctx.author.id
            and e.interaction.message.id == msg.id
            and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        try:
            res = await get_animal_image(animal)
        except:
            await msg.edit(f"API returned a `{res.status}` status :c", components=[])
            return

        embed = hikari.Embed(
            description=res["fact"],
            color=color,
        )
        embed.set_image(res["image"])

        animal = animal.replace("_", " ")

        await msg.edit(f"Here's a {animal} fact for you!", embed=embed, components=[])


@image.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="animal",
    description="Displays a cute animal image :3",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def animal(ctx: lightbulb.Context) -> None:
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

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
            predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.user.id == ctx.author.id
            and e.interaction.message.id == msg.id
            and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        animal = event.interaction.values[0]
        try:
            res = await get_animal_image(animal)
        except:
            await msg.edit(f"API returned a `{res.status}` status :c", components=[])
            return

        embed = hikari.Embed(
            color=color,
        )
        embed.set_image(res["image"])

        animal = animal.replace("_", " ")

        await msg.edit(f"Here's a cute {animal} for you!", embed=embed, components=[])


CANVAS = {
    "Pixelate": "👾",
    "Blur": "🌫",
    "YouTube": "🖥️",
    "Tweet": "💬",
    "Stupid": "🗿",
    "Simp": "🥺",
    "Horny": "🤤",
    "Lolice": f"{const.EMOJI_LOLICE}",
    "LGBTQ": "🏳️‍🌈",
    "Trans": "🏳️‍⚧️",
    "Oogway": f"{const.EMOJI_OOGWAY}",
}

c_items = {
    "pixelate": "https://some-random-api.ml/canvas/pixelate?avatar=$avatar",
    "blur": "https://some-random-api.ml/canvas/blur?avatar=$avatar",
    "youtube": "https://some-random-api.ml/canvas/youtube-comment?avatar=$avatar&username=$username&comment=$comment",
    "tweet": "https://some-random-api.ml/canvas/tweet?avatar=$avatar&username=$username&displayname=$displayname&comment=$comment",
    "stupid": "https://some-random-api.ml/canvas/its-so-stupid?avatar=$avatar&dog=im-stupid",
    "simp": "https://some-random-api.ml/canvas/simpcard?avatar=$avatar",
    "horny": "https://some-random-api.ml/canvas/horny?avatar=$avatar",
    "lolice": "https://some-random-api.ml/canvas/lolice?avatar=$avatar",
    "lgbtq": "https://some-random-api.ml/canvas/lgbt?avatar=$avatar",
    "trans": "https://some-random-api.ml/canvas/transgender?avatar=$avatar",
    "oogway": "https://some-random-api.ml/canvas/oogway?quote=$quote",
}


@image.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="text",
    description="Comment/Tweet/Make a quote, if you want to use the Youtube/Twitter/Oogway option",
    required=False,
    default="default text",
)
@lightbulb.command(
    name="canvas",
    description="Shows an image of the canvas you chose :3",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def canvas(ctx: lightbulb.Context, text: str) -> None | lightbulb.ResponseProxy:
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )
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
            predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.user.id == ctx.author.id
            and e.interaction.message.id == msg.id
            and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        misc = (event.interaction.values[0]).replace(" ", "")
        url = (
            (c_items[misc])
            .replace("$avatar", ctx.author.avatar_url.__str__())
            .replace("$comment", text)
            .replace("$quote", text)
            .replace("$username", ctx.author.username)
            .replace("$displayname", ctx.author.username)
        )
        if "comment" in url:
            url.replace(" ", "%20")
        embed = hikari.Embed(
            color=color,
        )
        embed.set_image(url)

        misc = misc.replace("_", " ")

        await msg.edit(f"Here's your {misc} canvas!", embed=embed, components=[])


OVERLAYS = {
    "Glass": "🪟",
    "Wasted": "⚰️",
    "Mission Passed": "⭐",
    "Jail": "🧑‍⚖️",
    "Comrade": "🪖",
    "Triggered": "💢",
}

o_items = {
    "glass": "https://some-random-api.ml/canvas/glass?avatar=$avatar",
    "wasted": "https://some-random-api.ml/canvas/wasted?avatar=$avatar",
    "mission_passed": "https://some-random-api.ml/canvas/passed?avatar=$avatar",
    "jail": "https://some-random-api.ml/canvas/jail?avatar=$avatar",
    "comrade": "https://some-random-api.ml/canvas/comrade?avatar=$avatar",
    "triggered": "https://some-random-api.ml/canvas/triggered?avatar=$avatar",
}


@image.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="overlay",
    description="Displays an overlay on your avatar :3",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def overlay(ctx: lightbulb.Context) -> None | lightbulb.ResponseProxy:
    member = ctx.member
    color = (
        c[0] if (c := [r.color for r in member.get_roles() if r.color != 0]) else None
    )

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
            predicate=lambda e: isinstance(e.interaction, hikari.ComponentInteraction)
            and e.interaction.user.id == ctx.author.id
            and e.interaction.message.id == msg.id
            and e.interaction.component_type == hikari.ComponentType.SELECT_MENU,
        )
    except asyncio.TimeoutError:
        await msg.edit("The menu timed out :c", components=[])
    else:
        overlay = event.interaction.values[0]
        url = o_items.get(overlay).replace("$avatar", ctx.author.avatar_url.__str__())
        embed = hikari.Embed(
            color=color,
        )
        embed.set_image(url)

        overlay = overlay.replace("_", " ")

        await msg.edit(f"Here's your {overlay} overlay!", embed=embed, components=[])


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(image)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(image)
