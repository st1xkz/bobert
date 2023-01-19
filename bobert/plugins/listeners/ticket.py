import hikari
import lightbulb
import miru
import toolbox

ticket = lightbulb.Plugin("ticket")


@ticket.listener(hikari.InteractionCreateEvent)
async def close_ticket(event: hikari.InteractionCreateEvent) -> None:
    if event.interaction.type is not hikari.InteractionType.MESSAGE_COMPONENT:
        return
    interaction: hikari.ComponentInteraction = event.interaction
    if interaction.custom_id == "close_ticket_button":
        ticket_owner = await event.app.d.pool.fetchval(
            "SELECT user_id FROM bobert_tickets WHERE channel_id = $1 ",
            interaction.channel_id,
        )
        mem = ticket.bot.cache.get_member(interaction.guild_id, interaction.user)
        if interaction.user.id == ticket_owner or (
            set(mem.role_ids).intersection({794401582514962473, 784497973950283827})
        ):
            await ticket.bot.d.pool.execute(
                "DELETE FROM bobert_tickets WHERE channel_id = $1",
                interaction.channel_id,
            )
            await interaction.create_initial_response(
                hikari.ResponseType.DEFERRED_MESSAGE_UPDATE, "Disabled ticket"
            )
            await ticket.bot.rest.edit_channel(interaction.channel_id, archived=True)
            await interaction.user.send(
                embed=hikari.Embed(
                    description=f"Here's your recent thread support channel <#{interaction.channel_id}>"
                )
            )


class TicketModal(miru.Modal):

    reason = miru.TextInput(
        label="Reason",
        style=hikari.TextInputStyle.PARAGRAPH,
        placeholder="Reason to the open the ticket.",
        max_length=500,
    )

    async def callback(self, context: miru.ModalContext) -> None:
        await context.defer()
        thread: hikari.GuildPrivateThread = await context.app.rest.create_thread(
            context.channel_id,
            type=hikari.ChannelType.GUILD_PRIVATE_THREAD,
            name=f"Ticket Help - {context.author}",
        )
        allow = (
            hikari.Permissions.SEND_MESSAGES
            | hikari.Permissions.ATTACH_FILES
            | hikari.Permissions.EMBED_LINKS
        )
        perms = [
            hikari.PermissionOverwrite(
                id=context.author.id,
                type=hikari.PermissionOverwriteType.MEMBER,
                allow=allow,
            )
        ]

        perms.extend(
            [
                hikari.PermissionOverwrite(
                    id=_id, type=hikari.PermissionOverwriteType.ROLE, allow=allow
                )
                for _id in [794401582514962473, 784497973950283827]
            ]
        )
        await thread.edit(permission_overwrites=perms)
        color = toolbox.get_member_color(context.get_guild().get_my_member())
        embed = hikari.Embed(
            title="Thanks for requesting support!",
            description=f"Hey {context.author.name}, this is your ticket! Please allow staff some time to read over your ticket summary and get back to you as soon as they can.",
            color=color,
        )
        embed.description += """

**Remember:**
• **No one** is obligated to answer you if they feel that you are trolling or misusing this ticket system.
• **Make sure** to be as clear as possible when explaining and provide as many details as you can.
• **Be patient** as we (staff members) have our own lives outside of Discord and we tend to get busy most days. We are human, so you should treat us as such!

Abusing/misusing this ticket system may result in punishment that varies from action to action.        
"""
        embed.add_field("Ticket Summary", self.reason.value)
        embed.set_footer(
            "This ticket may be closed at any time by you, an admin, or a staff member"
        )
        comp = (
            context.bot.rest.build_message_action_row()
            .add_button(hikari.ButtonStyle.DANGER, "close_ticket_button")
            .set_label("Close")
            .add_to_container()
        )
        await thread.send(
            content=f"{context.author.mention} <@&784497973950283827> <@&794401582514962473>",
            embed=embed,
            component=comp,
        )


class TicketButton(miru.View):
    async def view_check(self, context: miru.ViewContext) -> bool:
        if context.channel_id != 825445726783668234:
            return False

        if c_id := context.bot.d.pool.fetchval(
            "SELECT channel_id FROM bobert_tickets WHERE user_id = $1",
            context.author.id,
        ):
            await context.respond(
                embed=hikari.Embed(
                    description=f"You already have ticket opened in <#{c_id}>"
                )
            )
            return False

        return True

    @miru.button(label="Start Support", style=hikari.ButtonStyle.PRIMARY)
    async def support_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # Get open ticket list to check if member already has an open ticket
        await ctx.respond_with_modal(TicketModal("Create support"))


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket)
