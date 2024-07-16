from datetime import datetime

import hikari
import lightbulb

from bobert.core.utils.chron import format_dt

invite = lightbulb.Plugin("invites")


invite_tracker = {}


@invite.listener(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    invites = await invite.bot.rest.fetch_guild_invites(
        781422576660250634
    )  # Main server
    invite_tracker.update({invite.code: invite.uses for invite in invites})


@invite.listener(hikari.MemberCreateEvent)
async def on_invite_create(event: hikari.MemberCreateEvent):
    invites_before = invite_tracker.copy()
    invites_after = await invite.bot.rest.fetch_guild_invites(event.guild_id)

    for inv in invites_after:
        if inv.code in invites_before and inv.uses > invites_before[inv.code]:
            embed = hikari.Embed(
                title="Member Joined",
                description=f"{event.member.mention} joined the server",
                color=0xFFFFFF,
                timestamp=datetime.now().astimezone(),
            )
            embed.add_field(
                name="Invite URL:", value=f"https://discord.gg/{inv.code}", inline=False
            )
            embed.add_field(name="Invite Code:", value=f"`{inv.code}`", inline=True)
            embed.add_field(name="Uses:", value=str(inv.uses), inline=True)
            embed.add_field(
                name="Inviter:",
                value=f"{inv.inviter.mention} ({inv.inviter.id})",
                inline=False,
            )
            embed.add_field(
                name="Channel:",
                value=f"{inv.channel.mention} ({inv.channel.id})",
                inline=False,
            )
            embed.add_field(
                name="Invite Created On:",
                value=f"{format_dt(inv.created_at)} ({format_dt(inv.created_at, style='R')})",
                inline=False,
            )
            embed.add_field(
                name="Invite Expiration:", value=str(inv.max_uses), inline=True
            )
            embed.add_field(name="Invite Age:", value=str(inv.max_age), inline=True)
            embed.set_thumbnail(event.member.avatar_url)
            await invite.bot.rest.create_message(
                816800103829733416, embed=embed
            )  # Main server
            invite_tracker[inv.code] = inv.uses
            break


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(invite)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(invite)
