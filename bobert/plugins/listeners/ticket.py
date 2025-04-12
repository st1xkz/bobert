from datetime import datetime, timedelta

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
    def __init__(self, bot: hikari.GatewayBot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @miru.button(
        label="Close", style=hikari.ButtonStyle.DANGER, custom_id="close_ticket_button"
    )
    async def close_ticket(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        target = ctx.member
        if target is None:
            await ctx.respond("Member not found.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        guild = ctx.get_guild()
        if guild is None:
            await ctx.respond("Guild not found.", flags=hikari.MessageFlag.EPHEMERAL)
            return

        mem = guild.get_member(target.id) if guild else None

        color = (
            c[0]
            if (
                c := [
                    r.color for r in helpers.sort_roles(target.get_roles()) if r.color
                ]
            )
            else None
        )

        if target.id or (
            set(target.role_ids).intersection({TRAINEE_ROLE, STAFF_ROLE})
        ):
            await ctx.respond(
                "This support thread has been closed. If your question has not been answered or your issue not resolved, please create a new ticket in <#825445726783668234>."
            )
            await ticket.bot.rest.edit_channel(ctx.channel_id, archived=True)

            # view = miru.View()
            # view.add_item(miru.Button(label="Closed", disabled=True))
            # await ctx.edit_response(components=view)

            channel = await ticket.bot.rest.fetch_channel(ctx.channel_id)
            await ticket.bot.rest.create_message(
                LOGS_CH,
                embed=hikari.Embed(
                    description=f"{target.mention} has closed the support ticket named {channel.name}",
                    color=color,
                    timestamp=datetime.now().astimezone(),
                )
                .add_field(
                    name="Conversation",
                    value=f"[{channel.name}](https://discordapp.com/channels/{ctx.guild_id}/{ctx.channel_id})",
                )
                .set_author(name=str(target), icon=target.display_avatar_url)
                .set_footer(text=f"UID: {target.id}"),
            )
            await target.send(
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
                .set_thumbnail(guild.icon_url)
            )


class TicketModal(miru.Modal, title="Create a Support Ticket"):
    def __init__(self, bot: hikari.GatewayBot) -> None:
        super().__init__()
        self.bot = bot

    reason = miru.TextInput(
        label="Summary",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Provide some info for your support ticket",
        max_length=500,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        await ctx.defer()

        user = ctx.user

        thread = await self.bot.rest.create_thread(
            ctx.channel_id,
            hikari.ChannelType.GUILD_PRIVATE_THREAD,
            f"Ticket Help - {ctx.author.username}",
            auto_archive_duration=timedelta(days=3),
        )

        if isinstance(thread, hikari.GuildThreadChannel):
            allow_permissions = (
                hikari.Permissions.VIEW_CHANNEL
                | hikari.Permissions.SEND_MESSAGES
                | hikari.Permissions.EMBED_LINKS
                | hikari.Permissions.ATTACH_FILES
            )

            overwrites = [
                hikari.PermissionOverwrite(
                    id=user.id,
                    type=hikari.PermissionOverwriteType.MEMBER,
                    allow=allow_permissions,
                )
            ]

            staff_roles = [
                TRAINEE_ROLE,
                STAFF_ROLE,
            ]
            overwrites.extend(
                [
                    hikari.PermissionOverwrite(
                        id=hikari.Snowflake(role_id),
                        type=hikari.PermissionOverwriteType.ROLE,
                        allow=allow_permissions,
                    )
                    for role_id in staff_roles
                ]
            )

            await thread.edit(permission_overwrites=overwrites)

        target = ctx.member

        guild = ctx.get_guild()
        if guild:
            bot_member = guild.get_my_member()
            b_color = (
                toolbox.get_member_color(bot_member)
                if bot_member
                else hikari.Color(0x000000)
            )
        else:
            b_color = hikari.Color(0x000000)

        roles = target.get_roles() if target else []
        a_color = (
            c[0]
            if (c := [r.color for r in helpers.sort_roles(roles) if r.color])
            else None
        )

        embed = hikari.Embed(
            title="Thanks for requesting support!",
            description=f"Hey {target.display_name if target is not None else 'Unknown User'}, this is your ticket! Please allow staff some time to read over your ticket summary and get back to you as soon as they can.",
            color=b_color,
            timestamp=datetime.now().astimezone(),
        )
        embed.description = (
            (embed.description or "")
            + """
### Remember:
- **No one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.
- **Make sure** to be as clear as possible when explaining and provide as many details as you can.
- **Be patient** as we (staff members) have our own lives outside of Discord and we tend to get busy most days. We are human, so you should treat us as such!

Abusing/misusing this ticket system may result in punishment that varies from action to action.
        """
        )
        embed.add_field(
            name="Ticket Summary", value=self.reason.value or "No summary provided"
        )
        embed.set_footer(
            text="This ticket can be closed by you, a trainee, or a staff member at any time",
            icon=(target.display_avatar_url if target is not None else None),
        )
        comp = ticket.bot.rest.build_message_action_row().add_interactive_button(
            hikari.ButtonStyle.DANGER, "close_ticket_button", label="Close"
        )
        await thread.send(
            content=f"{target.mention if target else ''} <@&{TRAINEE_ROLE}> <@&{STAFF_ROLE}>",
            embed=embed,
            component=comp,
            user_mentions=True,
            role_mentions=True,
        )
        await ticket.bot.rest.create_message(
            LOGS_CH,
            embed=hikari.Embed(
                description=f"{target.mention if target else 'Unknown User'} has created a new support ticket",
                color=a_color,
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                name="Conversation",
                value=f"[{(await self.bot.rest.fetch_channel(thread.id)).name}](https://discordapp.com/channels/{ctx.guild_id}/{thread.id})",
            )
            .set_author(
                name=str(target),
                icon=(target.display_avatar_url if target is not None else None),
            )
            .set_footer(
                text=f"UID: {target.id if target is not None else 'Unknown ID'}"
            ),
        )


class TicketButton(miru.View):
    def __init__(self, bot: hikari.GatewayBot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    async def view_check(self, ctx: miru.ViewContext) -> bool:
        target = ctx.member
        if ctx.channel_id != HELP_CH:
            return False

        return True

    @miru.button(
        label="Start Support",
        style=hikari.ButtonStyle.PRIMARY,
        custom_id="start_support",
    )
    async def support_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond_with_modal(TicketModal(self.bot))


@ticket.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    view = TicketButton(ticket.bot)
    ticket.bot.d.miru.start_view(view)
    view1 = CloseTicket(ticket.bot)
    ticket.bot.d.miru.start_view(view1)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket)