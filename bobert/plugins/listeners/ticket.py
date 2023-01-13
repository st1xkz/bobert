import hikari
import lightbulb
import miru

ticket = lightbulb.Plugin("ticket")


class TicketButton(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    """
    Start support button interaction for TicketButton view

    Button params:
        label - button label
        style - button style
        function - support_button

    Check if interaction member already has an open ticket in db.
    If not exists, start new ticket process and add ID to db.
    Returns discord ui Modal to take in ticket summary

    Params:
        button - miru button
        interaction - miru interaction
    """

    @miru.button(label="Start Support", style=hikari.ButtonStyle.PRIMARY)
    async def support_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # Get open ticket list to check if member already has an open ticket
        ...


@ticket.command
@lightbulb.command(name="idk", description="this does stuff")
@lightbulb.implements(lightbulb.SlashCommand)
async def this_idk(ctx: lightbulb.Context) -> None:
    ...


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(ticket)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(ticket)
