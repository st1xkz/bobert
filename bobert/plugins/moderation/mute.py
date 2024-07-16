from datetime import datetime, timedelta

import hikari
import lightbulb
import miru

from bobert.core.utils import constants as const

mute = lightbulb.Plugin("mute")
mute.add_checks(lightbulb.has_roles(993695535556984873))

"""
TODO:
- Remove all user's roles when they get muted except for Muted (will need database)
  - Give all user's roles back when they get unmuted (will need database)
- Add duration to mute command (will need database)
 - Add duration to notification embed of mute
 - Strike/warn system
"""

# Main server ID
GUILD_ID = 781422576660250634


class MuteReason(miru.Modal, title="Mute Member"):
    reason = miru.TextInput(
        label="Reason",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Provide the reason for the mute",
        max_length=500,
    )

    def __init__(self, target: hikari.Member, role: hikari.Role):
        super().__init__()
        self.target = target
        self.role = role

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()

        await self.target.add_role(self.role.id)
        await ctx.respond(
            f"You have muted {self.target.mention}.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )

        # Send to mod-logs
        embed = hikari.Embed(
            title="Member Updated",
            description=f"{const.EMOJI_MUTE} A member {self.target.mention} has been muted",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Reason:",
            value=self.reason.value,
        )
        embed.set_author(
            name=f"Muted by {ctx.author} ({ctx.author.id})",
            icon=ctx.author.display_avatar_url,
        )
        embed.set_footer(text=f"UID: {self.target.id}")
        await mute.bot.rest.create_message(
            993698032463925398, embed=embed
        )  # Test server ID

        # Send to user's DMs
        embed = hikari.Embed(
            title="Member Mute",
            description="You have been muted in **Sage**. If you believe this mute was in error, you can appeal the decision in <#825445726783668234>.",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Reason:",
            value=self.reason.value,
        )
        embed.set_author(
            name=f"Muted by {ctx.author} ({ctx.author.id})",
            icon=ctx.author.display_avatar_url,
        )
        embed.set_footer(text=f"UID: {self.target.id}")
        await self.target.send(embed=embed)


@mute.command
@lightbulb.command(name="Mute", description="Mutes the user")
@lightbulb.implements(lightbulb.UserCommand)
async def mute_user(ctx: lightbulb.UserContext) -> None:
    if ctx.guild_id != GUILD_ID:
        return

    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
    role = next(
        (role for role in ctx.get_guild().get_roles().values() if role.name == "Muted"),
        None,
    )

    if target is None:
        await ctx.respond(
            "User not found or not in this server.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    if role is None:
        await ctx.respond(
            "Role not found or invalid role specified.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if role.id in target.role_ids:
        await ctx.respond(
            "This user is already muted.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    modal = MuteReason(target, role)
    builder = modal.build_response(ctx.bot.d.miru)
    await builder.create_modal_response(ctx.interaction)
    ctx.bot.d.miru.start_modal(modal)


class UnmuteReason(miru.Modal, title="Unmute Member"):
    reason = miru.TextInput(
        label="Reason",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Provide the reason for the unmute",
        max_length=500,
    )

    def __init__(self, target: hikari.Member, role: hikari.Role):
        super().__init__()
        self.target = target
        self.role = role

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()

        await self.target.remove_role(self.role.id)
        if self.role.id not in self.target.role_ids:
            await ctx.respond(
                "This user is not currently muted.", flags=hikari.MessageFlag.EPHEMERAL
            )
        else:
            await ctx.respond(
                f"You have unmuted {self.target.mention}.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )

            # Send to mod-logs
            embed = hikari.Embed(
                title="Member Mute Removed",
                description=f"{const.EMOJI_MUTE} A member {self.target.mention} has had their mute removed",
                color=0xFABD2F,
                timestamp=datetime.now().astimezone(),
            )
            embed.add_field(
                name="Reason:",
                value=self.reason.value,
            )
            embed.set_author(
                name=f"Removed by {ctx.author} ({ctx.author.id})",
                icon=ctx.author.display_avatar_url,
            )
            embed.set_footer(text=f"UID: {self.target.id}")
            await mute.bot.rest.create_message(
                993698032463925398, embed=embed
            )  # Test server ID

        # Send to user's DMs
        embed = hikari.Embed(
            title="Member Unmute",
            description="You have been unmuted in **Sage**",
            color=0xFABD2F,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Reason:",
            value=self.reason.value,
        )
        embed.set_author(
            name=f"Unmuted by {ctx.author} ({ctx.author.id})",
            icon=ctx.author.display_avatar_url,
        )
        embed.set_footer(text=f"UID: {self.target.id}")
        await self.target.send(embed=embed)


@mute.command
@lightbulb.command(name="Remove Mute", description="Removes the mute")
@lightbulb.implements(lightbulb.UserCommand)
async def unmute_user(ctx: lightbulb.UserContext) -> None:
    if ctx.guild_id != GUILD_ID:
        return

    target = ctx.app.cache.get_member(ctx.guild_id, ctx.options.target.id)
    role = next(
        (role for role in ctx.get_guild().get_roles().values() if role.name == "Muted"),
        None,
    )

    if target is None:
        await ctx.respond(
            "User not found or not in this server.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    if role is None:
        await ctx.respond(
            "Role not found or invalid role specified.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if role.id not in target.role_ids:
        await ctx.respond(
            "This user is not currently muted.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    modal = UnmuteReason(target, role)
    builder = modal.build_response(ctx.bot.d.miru)
    await builder.create_modal_response(ctx.interaction)
    ctx.bot.d.miru.start_modal(modal)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mute)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(mute)
