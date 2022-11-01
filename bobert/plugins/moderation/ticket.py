from datetime import datetime

import hikari
import lightbulb
import miru

from bobert.core.utils.check import check_attachments, check_message
from bobert.core.utils.db import get_ticket_data, update_ticket_data

ticket_plugin = lightbulb.Plugin("ticket")


class TicketButton(miru.View):

    """
    Start support button interaction for TicketButton view

    Button Params:
        • label = Button label
        • style = Button style (primary = discord blurple color)
        • Function = support_button

    Check if ctx member already has an open ticket in tickets.json.
    If not exists, start new ticket process and add member ID to json.
    Returns discord ui Modal to take in ticket summary.

    Params:
        • button = Miru Button
        • interaction = Miru Context
    """

    @miru.button(label="Start Support", style=hikari.ButtonStyle.PRIMARY)
    async def start_support(self, button: miru.Button, ctx: miru.Context):
        # Get open ticket list to check if member has an open ticket
        ticket_data = get_ticket_data()

        if ctx.author.id in ticket_data["open_ tickets"]:
            await ctx.respond(
                "You already have an open ticket! Please close the current one before starting another one.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return
        await ctx.respond_with_modal(modal=SupportModal(ticket_plugin.bot))


"""
Modal View (pop out window)

Modal View components

Params:
    • label = Text box title
    • placeholder = Summary box text, gets replaced when user starts typing
    • style = Textbox style (long input)
    • min_length = Required minimum character count in text box
    • max_length = Max character for the text box

Modal view

Params:
    • title = Modal window title
    • custom_id = Give the view a custom ID
    • components = Modal view components
"""


class SupportModal(miru.Modal):
    def __init__(self, bot):
        components = [
            miru.TextInput(
                label="Summary",
                placeholder="Provide some info for your support ticket",
                style=hikari.TextInputStyle.PARAGRAPH,
                min_length=1,
                max_length=500,
                required=True,
            )
        ]
        super().__init__(
            title="Create a Support Ticket",
            custom_id="create_ticket",
            components=components,
        )
        self.bot = bot

    """
    Modal interaction callback

    Gets the open tickets from tickets.json, checks modal interaction author against the returned list.
    If user ID exists in list, send ephemeral message, do not create thread/ticket.
    Otherwise, add user ID to list and update the ticket.json.
    Create new ticket/thread - Params: title, type: public

    Params:
        • ctx = Miru Context
    """

    async def callback(self, ctx: miru.ModalContext) -> None:
        ticket_summary = ctx.text_values["summary"]
        member = ctx.author
        guild_id = ctx.guild_id
        channel_id = ctx.channel_id

        guild = self.bot.get_guild(guild_id)
        log_channel = guild.get_channel(int(os.environ["LOG_CHANNEL"]))
        channel = guild.get_channel(channel_id)
        admin_role = guild.get_role(int(os.environ["ADMIN_ROLE"]))
        staff_role = guild.get_role(int(os.environ["STAFF_ROLE"]))
        color = (
            c[0]
            if (
                c := [
                    r.color
                    for r in ctx.get_guild().get_my_member().get_roles()
                    if r.color != 0
                ]
            )
            else None
        )
        # Update list of current open tickets
        ticket_data = get_ticket_data()
        ticket_data["open_tickets"].append(member.id)
        update_ticket_data(ticket_data)

        # Create the thread and initial embed message
        new_thread = await channel.create_thread(
            name=f"Ticket Help" - {member}, type=hikari.ChannelType.public_thread
        )

        embed = hikari.Embed(
            title="Thanks for Requesting Support!",
            description=f"""Hey {member.display_name}, this is your ticket! Please allow staff some time to read over your ticket summary and get back to you as soon as they can.

**Remember:**

 • **No one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.
 • **Make sure** to be as clear as possible when explaining and provide as many details as you can.
 • **Be patient** as we (staff members) have our own lives *outside of Discord* and we tend to get busy most days. We are human, so you should treat us as such!

Abusing/misusing this ticket system may result in punishment that varies from action to action.    
            """,
            color=color,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(name="Ticket Summary", value=ticket_summary, inline=False)
        embed.set_footer(
            text="This ticket may be closed at any time by you, an admin, or a staff member",
            icon=member.avatar_url or member.default_avatar_url,
        )
        # Send message to new thread, add CloseTicket interaction view button
        # Params: new_thread, member
        if staff_role == admin_role:
            await new_thread.respond(
                content=f"{member.mention}, {staff_role.mention}",
                embed=embed,
                view=CloseTicket(new_thread, member),
            )
        else:
            await new_thread.respond(
                content=f"{member.mention}, {staff_role.mention}, {admin_role.mention}",
                embed=embed,
                view=CloseTicket(new_thread, member),
            )
        # Required interaction response
        await ctx.respond(
            "Your ticket has been created.", flags=hikari.MessageFlag.EPHEMERAL
        )

        # Send embed to log channel
        embed = hikari.Embed(
            description=f"{member.mention} has created a new support thread",
            color=member.color,
            timestamp=datetime.now().astimezone(),
        )
        embed.add_field(
            name="Conversation",
            value=f"[{new_thread.name}](https://discordapp.com/channels/{guild.id}/{new_thread.id})",
        )
        embed.set_author(
            name=f"{member}", icon=member.avatar_url or member.default_avatar_url
        )
        embed.set_footer(text=f"{member.id}")
        await log_channel.respond(embed=embed)


"""
Close ticket interaction button view
Params: thread, member
"""


class CloseTicket(miru.View):
    def __init__(self, thread, member):
        self.thread = thread
        self.member = member

    """
    Interaction button for closing ticket/archiving thread
    Params: style: button color (red), custom_id: button id

    close_ticket function
    Pressing button will archive the thread (close the ticket), send a log message to log channel
    displaying who closed the ticket.

    Params:
        • button - Interaction button
        • interaction - Interaction callback when button is clicked
    """

    @miru.button(label="Close", style=hikari.ButtonStyle.DANGER, custom_id="close")
    async def close_ticket(self, button: miru.Button, ctx: miru.Context):
        guild = ctx.guild
        admin_role_id = int(os.environ["ADMIN_ROLE"])
        staff_role_id = int(os.environ["STAFF_ROLE"])
        admin_role = guild.get_role(admin_role_id)
        staff_role = guild.get_role(staff_role_id)
        log_channel = guild.get_channel(int(os.environ["LOG_CHANNEL"]))

        """
        Close ticket button can only be used by:
            • member that created the ticket
            • members with admin role
            • members with staff role
        """
        if (
            ctx.author == self.member
            or ctx.author == guild.owner
            or admin_role in ctx.author.roles
            or staff_role_id in ctx.author.roles
        ):
            embed = hikari.Embed(
                title="Support thread closed",
                description="""Your support thread has been closed.
If your question has not been answered or your issue is not resolved, please create a new support ticket in <#825445726783668234>.
                """,
                color=0x2F3136,
                timestamp=datetime.now().astimezone(),
            )
            embed.add_field(
                name="Conversation",
                value=f"[Jump to thread!](https://discordapp.com/channels/{ctx.guild.id}/{self.thread.id})",
            )
            if ctx.guild.icon:
                embed.set_thumbnail(ctx.guild.icon_url)

            await self.member.respond(embed=embed)
            await ctx.respond.send_message(
                "This support thread has been closed. If your question has not been answered or your issue not resolved, please create a new support ticket in <#825445726783668234>."
            )
            await self.thread.edit(archived=True)
            # Disable button after click
            self.stop()

            # Remove member from list of currently open tickets
            ticket_data = get_ticket_data()
            ticket_data["open_tickets"].remove(self.member.id)
            update_ticket_data(ticket_data)

            # Send log embed to log channel
            embed = hikari.Embed(
                description=f"{ctx.author.mention} has closed the support ticket named {self.thread.name}",
                color=ctx.author.color,
                timestamp=datetime.now().astimezone(),
            )
            embed.set_author(
                name=f"{ctx.author}",
                icon_url=ctx.user.avatar_url or ctx.user.default_avatar_url,
            )
            embed.add_field(
                name="Conversation",
                value=f"[{self.thread.name}](https://discordapp.com/channels/{ctx.guild.id}/{self.thread.id})",
            )
            embed.set_footer(text=f"User ID: {ctx.author.id}")
            await log_channel.respond(embed=embed)


@ticket_plugin.listener(hikari.GuildMessageCreateEvent)
async def on_ready(event: hikari.GuildMessageCreateEvent) -> None:
    self.bot.add_view(TicketButton(self.bot))


"""
on_message listener
Removes the auto-pinned message when a new thread is created.
Listens for DMs from bot owner to update the help channel embed message.
Takes a channel ID, message ID message, splits the message and fetches the channel and message
Params:
    • message - The message object
Message must include a comma separated channel ID, message ID, and the uploaded sample.json file
"""


@ticket_plugin.listener(hikari.GuildMessageCreateEvent)
async def on_message(self, event: hikari.GuildMessageCreateEvent):
    if event.author.bot and event.type != hikari.MessageType.thread_created:
        return

    guild = event.guild
    owner = guild.owner
    channel = message.channel
    help_channel = guild.get_channel(int(os.environ["HELP_CHANNEL"]))
    admin_role = guild.get_role(int(os.environ["ADMIN_ROLE"]))
    help_channel = await self.bot.fetch_channel(int(os.environ["HELP_CHANNEL"]))

    if channel == help_channel:
        # Auto-delete the "new thread" message
        if event.type == hikari.MessageType.thread_created:
            await event.delete()
            return

        if event.author == owner or admin_role in event.author.roles:
            """
            Add new embed to the channel - only attach file with an empty message
            file must be the edited sample.json file
            """
            if event.content == "":
                """
                Message content is empty - new embed
                check for correct file criteria, must be 1 file
                must be the sample.json
                """
                embed = await check_attachments(event)

                if embed == "Error":
                    await channel.respond(
                        "Please check the sample.json for proper formatting.",
                        flags=hikari.MessageFlag.EPHEMERAL,
                    )
                elif embed is None:
                    await channel.respond(
                        "No supported file was uploaded.",
                        flags=hikari.MessageFlag.EPHEMERAL,
                    )
                else:
                    await channel.respond(embed=embed, view=TicketButton(self.bot))
                await event.delete()

            else:
                """
                Message content is not empty, should be a message ID only.
                Check attachments, and check message ID to confirm it's a message.
                If no errors, update embed in channel.
                """
                msg = await check_message(event)
                embed = await check_attachments(event)

                if msg == "Error":
                    await channel.respond(
                        "No channel with that ID was found",
                        flags=hikari.MessageFlag.EPHEMERAL,
                    )
                else:
                    if embed is None:
                        await channel.respond(
                            "No supported file was uploaded.",
                            flags=hikari.MessageFlag.EPHEMERAL,
                        )
                    elif embed == "Error":
                        await channel.respond(
                            "Please check the sample.json for formatting issues.",
                            flags=hikari.MessageFlag.EPHEMERAL,
                        )
                    else:
                        await msg.edit(content=None, embed=embed)
                await event.delete()


# Command for downloading sample.json - requires admin or owner
@ticket_plugin.command
@lightbulb.command(name="sample", description="Download sample", hidden=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def download_sample(ctx: lightbulb.Context) -> None:
    guild = ctx.guild
    owner = guild.owner
    member = ctx.author
    admin_role = guild.get_role(int(os.environ["ADMIN_ROLE"]))

    if member == owner or admin_role in member.roles:
        await ctx.send(
            "Check your DM for the sample file.", flags=hikari.MessageFlag.EPHEMERAL
        )
        await member.send(file=hikari.File("./sample.json"))
    else:
        await ctx.send(
            "You do not have permission to use this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket_plugin)
