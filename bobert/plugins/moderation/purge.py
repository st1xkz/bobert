import datetime

import hikari
import lightbulb
import miru

from bobert.core.utils import constants as const

purge = lightbulb.Plugin("purge")
purge.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))


class PurgeButton(miru.View):
    def __init__(self, amount) -> None:
        super().__init__()
        self.amount = amount

    @miru.button(
        label="Confirm",
        emoji=hikari.Emoji.parse(const.EMOJI_POSITIVE),
        style=hikari.ButtonStyle.SUCCESS,
    )
    async def confirm_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        # Fetches messages that are not older than 14 days in the channel the command is invoked in
        await ctx.defer()
        messages = (
            await purge.bot.rest.fetch_messages(ctx.channel_id)
            .take_until(
                lambda m: datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=14)
                > m.created_at
            )
            .limit(self.amount)
        )
        if messages:
            await purge.bot.rest.delete_messages(ctx.channel_id, messages)
            await ctx.edit_response(
                f"👍 Purged **{len(messages)}** messages.",
                flags=hikari.MessageFlag.EPHEMERAL,
                components=[],
            )
        else:
            await ctx.edit_response(
                "⚠️ Could not find any messages younger than 14 days!",
                flags=hikari.MessageFlag.EPHEMERAL,
                components=[],
            )

    @miru.button(
        label="Cancel",
        emoji=hikari.Emoji.parse(const.EMOJI_NEGATIVE),
        style=hikari.ButtonStyle.DANGER,
    )
    async def cancel_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        # When user clicks 'cancel' button, send confirmation message
        await ctx.defer()
        await ctx.edit_response(
            "👍 The purge operation has been cancelled.",
            flags=hikari.MessageFlag.EPHEMERAL,
            components=[],
        )


@purge.command()
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    "amount", "the amount of messages to purge", type=int, max_value=100, min_value=1
)
@lightbulb.command(
    "purge", "Purge a certain amount of messages from a channel", pass_options=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def _purge(ctx: lightbulb.SlashContext, amount: int) -> None:
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(
            lambda m: datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(days=14)
            > m.created_at
        )
        .limit(amount)
    )

    view = PurgeButton(amount)
    await ctx.respond(
        f"Are you sure you would like to purge **{len(messages)}** messages in this channel?",
        flags=hikari.MessageFlag.EPHEMERAL,
        components=view.build(),
    )
    ctx.bot.d.miru.start_view(view)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge)
