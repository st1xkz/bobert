from datetime import datetime

import hikari
import lightbulb
import miru
import toolbox

from bobert.core.utils import helpers

ticket = lightbulb.Plugin("ticket")

LOGS_CH = 942522981215793182
HELP_CH = 825445726783668234
STAFF_ROLE = 794401582514962473
TRAINEE_ROLE = 1087787891893227741


class CloseTicket(miru.View):
    @miru.button(
        label="Close", style=hikari.ButtonStyle.DANGER, custom_id="close_ticket_button"
    )
    async def close_ticket(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        target = ctx.member
        ticket_owner = await ctx.bot.d.ticket_pool.fetchval(
            "SELECT user_id FROM bobert_tickets WHERE channel_id = $1 ", ctx.channel_id
        )
        mem = ticket.bot.cache.get_member(ctx.guild_id, target)
        color = (
            c[0]
            if (
                c := [
                    r.color for r in helpers.sort_roles(target.get_roles()) if r.color
                ]
            )
            else None
        )

        if target == ticket_owner or (
            set(mem.role_ids).intersection({TRAINEE_ROLE, STAFF_ROLE})
        ):
            await ticket.bot.d.ticket_pool.execute(
                "DELETE FROM bobert_tickets WHERE channel_id = $1",
                ctx.channel_id,
            )
            await ctx.respond(
                "This support thread has been closed. If your question has not been answered or your issue not resolved, please create a new ticket in <#825445726783668234>."
            )
            await ticket.bot.rest.edit_channel(ctx.channel_id, archived=True)
            await ctx.bot.rest.create_message(
                LOGS_CH,
                embed=hikari.Embed(
                    description=f"{target.mention} has closed the support ticket named {(await ctx.bot.rest.fetch_channel(ctx.channel_id)).name}",
                    color=color,
                    timestamp=datetime.now().astimezone(),
                )
                .add_field(
                    name="Conversation",
                    value=f"[{(await ctx.bot.rest.fetch_channel(ctx.channel_id)).name}](https://discordapp.com/channels/{ctx.guild_id}/{ctx.channel_id})",
                )
                .set_author(name=str(target), icon=target.display_avatar_url)
                .set_footer(text=f"UID: {target.id}"),
            )
            await ctx.bot.cache.get_user(ticket_owner).send(
                embed=hikari.Embed(
                    title="Support thread closed",
                    description="""Your support thread has been closed.
If your question has not been answered or your issue not resolved, please create a new ticket in <#825445726783668234>.
                    """,
                    color=0x2F3136,
                )
                .add_field(
                    name="Conversation",
                    value=f"[Jump to thread!](https://discordapp.com/channels/{ctx.guild_id}/{ctx.channel_id})",
                )
                .set_thumbnail(ctx.get_guild().icon_url)
            )


class TicketModal(miru.Modal):
    reason = miru.TextInput(
        label="Summary",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Provide some info for your support ticket",
        max_length=500,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()
        thread: hikari.GuildPrivateThread = await ctx.app.rest.create_thread(
            ctx.channel_id,
            hikari.ChannelType.GUILD_PRIVATE_THREAD,
            f"Ticket Help - {ctx.author}",
        )
        allow = (
            hikari.Permissions.SEND_MESSAGES
            | hikari.Permissions.ATTACH_FILES
            | hikari.Permissions.EMBED_LINKS
        )
        perms = [
            hikari.PermissionOverwrite(
                id=ctx.author.id,
                type=hikari.PermissionOverwriteType.MEMBER,
                allow=allow,
            )
        ]

        perms.extend(
            [
                hikari.PermissionOverwrite(
                    id=_id, type=hikari.PermissionOverwriteType.ROLE, allow=allow
                )
                for _id in [TRAINEE_ROLE, STAFF_ROLE]
            ]
        )
        await thread.edit(permission_overwrites=perms)
        await ticket.bot.d.ticket_pool.execute(
            "INSERT INTO bobert_tickets VALUES ($1, $2)", ctx.author.id, thread.id
        )
        target = ctx.member
        b_color = toolbox.get_member_color(ctx.get_guild().get_my_member())
        a_color = (
            c[0]
            if (
                c := [
                    r.color for r in helpers.sort_roles(target.get_roles()) if r.color
                ]
            )
            else None
        )
        embed = hikari.Embed(
            title="Thanks for requesting support!",
            description=f"Hey {target.display_name}, this is your ticket! Please allow staff some time to read over your ticket summary and get back to you as soon as they can.",
            color=b_color,
            timestamp=datetime.now().astimezone(),
        )
        embed.description += """

**Remember:**
- **No one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.
- **Make sure** to be as clear as possible when explaining and provide as many details as you can.
- **Be patient** as we (staff members) have our own lives outside of Discord and we tend to get busy most days. We are human, so you should treat us as such!

Abusing/misusing this ticket system may result in punishment that varies from action to action.        
"""
        embed.add_field("Ticket Summary", self.reason.value)
        embed.set_footer(
            "This ticket can be closed by you, a trainee, or a staff member at any time",
            icon=target.display_avatar_url,
        )
        comp = ctx.bot.rest.build_message_action_row().add_interactive_button(
            hikari.ButtonStyle.DANGER, "close_ticket_button", label="Close"
        )
        await thread.send(
            content=f"{target.mention} <@&{TRAINEE_ROLE}> <@&{STAFF_ROLE}>",
            embed=embed,
            component=comp,
            user_mentions=True,
            role_mentions=True,
        )
        await ctx.bot.rest.create_message(
            LOGS_CH,
            embed=hikari.Embed(
                description=f"{target.mention} has created a new support ticket",
                color=a_color,
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                name="Conversation",
                value=f"[{(await ctx.bot.rest.fetch_channel(thread.id)).name}](https://discordapp.com/channels/{ctx.guild_id}/{thread.id})",
            )
            .set_author(name=str(target), icon=target.display_avatar_url)
            .set_footer(text=f"UID: {target.id}"),
        )


class TicketButton(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def view_check(self, ctx: miru.ViewContext) -> bool:
        target = ctx.member
        if ctx.channel_id != HELP_CH:
            return False

        if c_id := await ticket.bot.d.ticket_pool.fetchval(
            "SELECT channel_id FROM bobert_tickets WHERE user_id = $1",
            target.id,
        ):
            await ctx.respond(
                "You already have an open ticket! Please close the current one before starting another.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return False

        return True

    @miru.button(
        label="Start Support",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="start_support",
    )
    async def support_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        # Get open ticket list to check if member already has an open ticket
        await ctx.respond_with_modal(TicketModal("Create a Support Ticket"))


@ticket.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    view = TicketButton()
    ticket.bot.d.miru.start_view(view)
    view1 = CloseTicket(timeout=None)
    ticket.bot.d.miru.start_view(view1)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket)
