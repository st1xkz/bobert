import asyncio
import io
from datetime import datetime

import hikari
import lightbulb
from PIL import Image

color = lightbulb.Plugin("color")


@color.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="hex_code",
    description="the hex code to the specified color",
    required=True,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="get-color",
    description="Displays color of specified hex code (you can add up to 10)",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_color(ctx: lightbulb.Context) -> None:
    color_codes = ctx.options.hex_code.split()
    size = (60, 80) if len(color_codes) > 1 else (200, 200)

    if len(color_codes) > 10:
        return await ctx.respond(
            "You can only supply a maximum of **10** hex codes.", delete_after=10
        )

    for color_code in color_codes:
        if not color_code.startswith("#"):
            colour_code = "#" + color_code
            image = Image.new("RGB", size, colour_code)
            buf = io.BytesIO()

            with buf as file:
                image.save(file, "PNG")
                file.seek(0)

                embed = hikari.Embed(
                    title=f"Color `{colour_code}`",
                    color=0x2F3136,
                    timestamp=datetime.utcnow().astimezone(),
                )
                embed.set_image(hikari.Bytes(file, "Color.png"))
                embed.set_footer(text=f"Requested by {ctx.author}")
                await ctx.respond(embed=embed)
            await asyncio.sleep(1)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(color)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(color)
