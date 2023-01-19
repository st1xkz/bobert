import datetime

import hikari
import lightbulb
import miru

from bobert.core.utils import constants as const

purge = lightbulb.Plugin("purge")
purge.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_MESSAGES))


class PurgeButton(miru.View):
    def __init__(self, amount) -> None:
        self.amount = amount

    @miru.button(
        label="Confirm", emoji=const.EMOJI_CONFIRM, style=hikari.ButtonStyle.SUCCESS
    )
    async def confirm_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # When user clicks 'confirm' button, delete amount of messages user entered
        # Fetch messages that are not older than 14 days in the channel the command is invoked in
        # Messages older than 14 days cannot be deleted by bots, so this is a necessary precaution
        messages = (
            await ctx.app.rest.fetch_messages(ctx.channel_id)
            .take_until(
                lambda m: datetime.datetime.now(datetime.timezone.utc)
                - datetime.timedelta(days=14)
                > m.created_at
            )
            .limit(self.amount)
        )
        if messages:
            await ctx.app.rest.delete_messages(ctx.channel_id, messages)
            await ctx.edit_message(
                f"👍 Purged **{len(messages)}** messages.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        else:
            await ctx.edit_message(
                "⚠️ Could not find any messages younger than 14 days!",
                flags=hikari.MessageFlag.EPHEMERAL,
            )

    @miru.button(
        label="Cancel", emoji=const.EMOJI_CANCEL, style=hikari.ButtonStyle.DANGER
    )
    async def cancel_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
        # When user clicks 'cancel' button, send message saying command is cancelled
        await ctx.edit_message(
            "👍 The purge operation has been cancelled.",
            flags=hikari.MessageFlag.EPHEMERAL,
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
        .limit(self.amount)
    )

    view = PurgeButton(amount)
    res = await ctx.respond(
        f"Are you sure you would like to purge **{len(messages)}** messages from the channel?",
        flags=hikari.MessageFlag.EPHEMERAL,
        components=view.build(),
    )
    view.start(res)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(purge)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(purge)
