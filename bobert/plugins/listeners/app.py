from datetime import datetime

import hikari
import lightbulb
import miru

from bobert.core.utils import helpers

app = lightbulb.Plugin("app")

"""
TODO:
- Fix type check errors
- Add select menus for team positions (Event Host, Event Assistant, Trainee) instead
  of having "Start App" button
- Transform select menu into modal
- Add general questions to match all team roles
"""


class AppButton(miru.View):
    # Create approve and reject buttons for app modal
    @miru.button(
        label="Approve", style=hikari.ButtonStyle.SUCCESS, custom_id="approve_button"
    )
    async def approve_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        target = app.bot.cache.get_user(
            int(ctx.interaction.message.embeds[0].footer.text.split("UID: ")[1])
        )
        await ctx.defer()
        embed = hikari.Embed(
            title="Congratulations! Your Staff Application has been Approved!",
            description=f"Hello {target},\n\nWe're excited to inform you that your staff application has been approved! 🎉",
            color=0xFFFFFF,
        )
        embed.add_field(
            name="What to Expect:",
            value="""
- You'll receive the **Trainees** role shortly, granting you to staff-exclusive channels and trainee-specific privileges.
- Our staff team will reach out to provide additional information about your role and responsibilities during the training period.
- Please review our server guidelines and familiarize yourself with our rules to maintain a positive and welcoming community.
            """,
        )
        embed.add_field(
            name="Training Period:",
            value="""
- As a Trainee, you'll have the opportunity to learn and grow within our staff team. We'll provide guidance and mentorship to help you succeed.
- During your training, you'll work closely with experienced staff members and gain valuable experience in server moderation.
            """,
        )
        embed.add_field(
            name="Next Steps:",
            value=f"""
- Be prepared to contribute positively to our server and help us maintain a friendly environment.
- If you have any questions or need assistance, feel free to reach out to a staff member.

Once again, congratulations, and welcome to the Sage staff team as a Trainee! We look forward to working with you and watching you grow in your role. As a Trainee, you'll have the opportunity to learn and prove yourself. Your dedication and contributions may lead to future promotions within our staff team.

We're excited to see your potential and how you'll positively impact our community.

Best regards,
{ctx.member}
Sage Staff Team
            """,
        )
        embed.set_author(name="🔔 Important Notice")
        await target.send(embed=embed)

        existing_embed = ctx.interaction.message.embeds[0]

        if ctx.interaction.custom_id == "approve_button":
            existing_embed.set_thumbnail(
                "https://cdn.discordapp.com/emojis/1059009032876199976.png"
            )

        view = miru.View()
        view.add_item(
            miru.Button(
                label="Application Approved",
                style=hikari.ButtonStyle.SUCCESS,
                disabled=True,
            )
        )
        await ctx.edit_response(embeds=[existing_embed], components=view)

    @miru.button(
        label="Reject", style=hikari.ButtonStyle.DANGER, custom_id="reject_button"
    )
    async def reject_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        target = app.bot.cache.get_user(
            int(ctx.interaction.message.embeds[0].footer.text.split("UID: ")[1])
        )
        await ctx.defer()
        embed = hikari.Embed(
            title="Regarding Your Staff Application for Sage",
            description=f"""
We appreciate your interest in joining the Sage staff team and for taking the time to submit your application.

We regret to inform you that, after careful consideration, your staff application has not been successful at this time. We understand this may be disappointing, but please know that this decision does not reflect your worth as a member of our community.
            """,
            color=0xFFFFFF,
        )
        embed.add_field(
            name="Feedback:",
            value="""
While we cannot accept your application at this time, we value your commitment to our server. We encourage you to review our server's staff requirements and qualifications in <#1085754764693885008>. If you wish, we would be happy to provide feedback on your application to help you improve for future opportunities. Please let us know if you would like to receive feedback.
            """,
        )
        embed.add_field(
            name="Reapplying:",
            value=f"""
We encourage you to continue being an active and positive member of our community. Opportunities to join the staff team may arise in the future, and we would welcome your application at that time.

If you have any questions or need further information, please feel free to reach out to a staff member.

Thank you for being a part of our community, and we hope to see you continue to contribute positively to Sage.

Best regards,
{ctx.member}
Sage Staff Team
            """,
        )
        embed.set_author(name="🔔 Important Notice")
        await target.send(embed=embed)

        existing_embed = ctx.interaction.message.embeds[0]

        if ctx.interaction.custom_id == "reject_button":
            existing_embed.set_thumbnail(
                "https://cdn.discordapp.com/emojis/1059009054044864532.png"
            )

        view = miru.View()
        view.add_item(
            miru.Button(
                label="Application Rejected",
                style=hikari.ButtonStyle.DANGER,
                disabled=True,
            )
        )
        await ctx.edit_response(embeds=[existing_embed], components=view)


class AppModal(miru.Modal):
    intro = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Tell us about yourself.",
        placeholder="Introduce yourself. Share your skills, timezone, or any personal details.",
        required=True,
    )
    motive = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Why do you want to join our staff team?",
        placeholder="Help us understand what your motivations are.",
        required=True,
    )
    exp = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="What relevant experience/skills do you have?",
        placeholder="Highlight qualifications, including mod, leadership, and technical skills (e.g., bot management).",
        required=True,
    )
    resolution = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="How would you handle conflict in the server?",
        placeholder="Put yourself in a scenario where your problem-solving and conflict resolution skills are used.",
        required=True,
    )
    improvement = miru.TextInput(
        style=hikari.TextInputStyle.PARAGRAPH,
        label="Ideas/improvements if selected?",
        placeholder="Showcase your creativity and commitment to server improvement.",
        required=True,
    )

    async def callback(self, ctx: miru.ModalContext) -> None:
        view = AppButton()
        target = ctx.member

        color = (
            c[0]
            if (
                c := [
                    r.color for r in helpers.sort_roles(target.get_roles()) if r.color
                ]
            )
            else None
        )

        await app.bot.rest.create_message(
            1088960253565095986,
            components=view,
            embed=hikari.Embed(
                color=color,
                timestamp=datetime.now().astimezone(),
            )
            .add_field(
                name="1. Tell us about yourself",
                value=self.intro.value,
                inline=False,
            )
            .add_field(
                name="2. Why do you want to join our staff team?",
                value=self.motive.value,
                inline=False,
            )
            .add_field(
                name="3. What relevant experience/skills do you have?",
                value=self.exp.value,
                inline=False,
            )
            .add_field(
                name="4. How would you handle conflict in the server?",
                value=self.resolution.value,
                inline=False,
            )
            .add_field(
                name="5. Ideas/improvements if selected?",
                value=self.improvement.value,
                inline=False,
            )
            .set_author(
                name=f"Staff Application - {str(target)}",
                icon=target.display_avatar_url,
            )
            .set_footer(text=f"UID: {target.id}"),
        )

        ctx.client.start_view(view)
        await ctx.respond(
            "Your application was submitted successfully!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )


class StartAppButton(miru.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    # Create a new view (button) that will invoke the AppModal
    @miru.button(
        label="Start Staff Application",
        style=hikari.ButtonStyle.SECONDARY,
        custom_id="start_app_button",
    )
    async def app_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond_with_modal(AppModal("Staff Applcation Form"))


@app.listener(hikari.StartedEvent)
async def start_button(event: hikari.StartedEvent) -> None:
    view = StartAppButton()
    app.bot.d.miru.start_view(view)

    view1 = AppButton(timeout=None)
    app.bot.d.miru.start_view(view1, bind_to=None)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(app)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(app)
