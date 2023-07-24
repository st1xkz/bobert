import hikari
import lightbulb
import miru

app = lightbulb.Plugin("app")


class AppModal(miru.Modal):
    name = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Discord Username",
        placeholder="E.g. JohnnyAppleseed",
        required=True,
    )
    _id = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Discord ID.",
        placeholder="E.g. 353922343020690884",
        required=True,
    )
    level = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Current level.",
        placeholder="E.g. Type !rank in the bots channel to see what level you're at.",
        required=True,
    )
    mic = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH, label="Do you have a mic?", required=True
    )
    joined = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Server join date.",
        placeholder="E.g. I've been on this server for X amount of time.",
        required=True,
    )
    exp = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Previous staff roles?",
        placeholder="E.g. I've been a moderator in XYZ server with 10 members.",
        required=True,
    )
    sit = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Dealing with tough situations.",
        placeholder="E.g. Tackled rule-breaking user on gaming server with NSFW spam. Gave warnings, temp ban, and plan.",
        required=True,
    )
    rules = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Server rules familiarity.",
        placeholder="E.g. Familiar with server rules as mod. Updated with changes to enforce consistently and fairly.",
        required=True,
    )
    diff = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Handling rule breakers.",
        placeholder="E.g. I'd give them some warnings and if they keep doing it, I'd mute them.",
        required=True,
    )
    describe = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Describe yourself.",
        placeholder="E.g. Some info you can share is your age, time zone, and continent. Interests are welcome.",
        required=True,
    )
    mod = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Why join the mod team?",
        placeholder="E.g. I want to contribute as mod, have skills to make server welcoming.",
        required=True,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        target = ctx.member
        msg = await app.bot.rest.create_message(
            1088960253565095986,
            embed=hikari.Embed(
                timestamp=datetime.now().astimezone(),
            )
            .add_field(name="1. Discord Username", value=self.name.value, inline=False)
            .add_field(name="2. Discord ID.", value=self._id.value, inline=False)
            .add_field(name="3. Current level.", value=self.level.value, inline=False)
            .add_field(name="4. Do you have a mic?", value=self.mic.value, inline=False)
            .add_field(
                name="5. Server join date.",
                value=self.joined.value,
                inline=False,
            )
            .add_field(
                name="6. Previous staff roles?",
                value=self.exp.value,
                inline=False,
            )
            .add_field(
                name="7. Dealing with tough situations.",
                value=self.sit.value,
                inline=False,
            )
            .add_field(
                name="8. Server rules familiarity.",
                value=self.rules.value,
                inline=False,
            )
            .add_field(
                name="9. Handling rule breakers.",
                value=self.diff.value,
                inline=False,
            )
            .add_field(
                name="10. Describe yourself.", value=self.describe.value, inline=False
            )
            .add_field(
                name="11. Why join the mod team?",
                value=self.mod.value,
                inline=False,
            )
            .set_author(name=target, icon=target.display_avatar_url),
        )


class StartAppButton(miru.View):
    # Create a new view (button) that will invoke the AppModal
    @miru.button(label="Start Staff Application", style=hikari.ButtonStyle.SECONDARY)
    async def app_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        modal = AppModal()
        await ctx.respond(
            "Click the button below to start the staff application process.",
            modal,
            flags=hikari.MessageFlags.EPHEMERAL,
        )


class AppButton(miru.View):
    # Create approve and reject buttons for app modal
    @miru.button(
        label="Approve", style=hikari.ButtonStyle.SUCCESS, custom_id="approve_button"
    )
    async def approve_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        await ctx.bot.rest.create_message(
            1088960253565095986,
            embed=hikari.Embed(description="Application Approved!", color=0x00FF00),
        )

    @miru.button(
        label="Reject", style=hikari.ButtonStyle.DANGER, custom_id="reject_button"
    )
    async def reject_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        await ctx.defer()
        await ctx.bot.rest.create_message(
            1088960253565095986,
            embed=hikari.Embed(description="Application Rejected!", color=0xFF0000),
        )


@app.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    view = StartAppButton()
    await view.start()
    view1 = AppButton(timeout=None)
    await view1.start()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(app)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(app)
