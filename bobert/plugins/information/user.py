import typing as t

import hikari
import lightbulb
import miru

from bobert.core.utils import helpers

user = lightbulb.Plugin("member")
user.add_checks(lightbulb.checks.guild_only)


class AvatarButton(miru.View):
    def __init__(self, target) -> None:
        super().__init__()
        self.target = target

    @miru.button(label="Global Avatar", emoji="🌎", style=hikari.ButtonStyle.SECONDARY)
    async def global_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.defer()
        target = self.target

        embed = hikari.Embed(
            title=f"{target}",
            description=f"[**Global Avatar URL**]({target.avatar_url})",
        )
        embed.set_image(target.avatar_url)
        await ctx.edit_response(embed=embed, content=None, components=[])

    @miru.button(
        label="Server Avatar", emoji="🧑‍🤝‍🧑", style=hikari.ButtonStyle.SECONDARY
    )
    async def server_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.defer()
        target = self.target
        color = (
            c[0]
            if (
                c := [
                    r.color for r in helpers.sort_roles(target.get_roles()) if r.color
                ]
            )
            else None
        )
        at = "Server" if target.guild_avatar_url else "Global"

        embed = hikari.Embed(
            title=f"{target}",
            description=f"[**{at} Avatar URL**]({target.display_avatar_url})",
            color=color,
        )
        embed.set_image(target.display_avatar_url)
        await ctx.edit_response(embed=embed, content=None, components=[])


@user.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=False,
)
@lightbulb.command(
    name="avatar",
    description="Shows your own or another user's avatar",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def avatar_cmd(
    ctx: lightbulb.SlashContext, member: t.Optional[hikari.Member] = None
) -> None:
    """Allows mentioning of a member or to use the ID of theirs when using the member option."""
    if member is None:
        member = ctx.member

    target = ctx.bot.cache.get_member(ctx.guild_id, member.id)  # type: ignore

    if not target:
        await ctx.respond(
            "❌ The user you specified isn't in the server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    view = AvatarButton(target)
    await ctx.respond(
        f"Choose the type of avatar from {target.mention} to view!",
        components=view.build(),
    )
    ctx.bot.d.miru.start_view(view)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(user)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(user)
