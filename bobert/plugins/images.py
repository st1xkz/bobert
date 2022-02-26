import hikari
import lightbulb

import io

plugin = lightbulb.Plugin("images")

@plugin.command
@lightbulb.add_cooldown(10, 3, bucket=lightbulb.cooldowns.UserBucket)
@lightbulb.option("message", "the text you want to write!", type=str, required=True, modifier=lightbulb.commands.OptionModifier.CONSUME_REST)
@lightbulb.option("member", "the name of the user!", hikari.Member, required=True)
@lightbulb.command(name="tweet", description="create a fake tweet", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def tweet_command(ctx: lightbulb.Context) -> None:
    parameters = {
        "avatar" : ctx.options.member.avatar_url or ctx.options.member.default_avatar_url,
        "username" : ctx.options.member.username,
        "displayname" : ctx.options.member.display_name or ctx.options.member.username,
        "comment" : ctx.options.message
    }
    
    async with ctx.bot.d.aio_session.get(
        f'https://some-random-api.ml/canvas/tweet',
        params=parameters
    ) as res:
            imageData = io.BytesIO(await res.read())
            imageData.seek(0)
        
            embed = hikari.Embed(
                    color=0xf1f1f1,
                )
            embed.set_image(imageData)
            await ctx.respond(embed)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)