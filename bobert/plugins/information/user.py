import hikari
import lightbulb

from datetime import datetime


user_plugin = lightbulb.Plugin("user")


@user_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="The Discord member",
    type=hikari.User,
    required=False,
)
@lightbulb.command(
    name="userinfo",
    aliases=["user", "whois", "ui"],
    description="Displays info about a user",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_user(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())
    target_status = (
        target.get_presence().visible_status if target.get_presence() else "Offline"
    )

    roles = (await target.fetch_roles())[1:]

    embed = (
        hikari.Embed(
            title=f"User Info - {target.username}#{target.discriminator}",
            description=f"ID: `{target.id}`",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Nickname",
            f"{target.nickname}",
            inline=True,
        )
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Status",
            f"{target_status.title()}",
            inline=True,
        )
        .add_field(
            "Boosted?",
            f"{target.premium_since}",
            inline=True,
        )
        .add_field(
            "Account Created",
            f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=False,
        )
        .add_field(
            "Joined",
            f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline=False,
        )
        .add_field(
            f"Roles [{len(roles)}]",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
        .set_thumbnail(
            target.avatar_url or target.default_avatar_url,
        )
        .set_footer(
            text=f"Requested by {ctx.member.username}#{ctx.member.discriminator}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url
        )
    )
    await ctx.respond(embed)


@user_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.User,
    required=False,
)
@lightbulb.command(
    name="banner",
    description="Displays the member's banner",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_banner(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    banner = target.banner_url
    if banner:
        embed = (
            hikari.Embed(
                title="Banner Viewer",
                description=f"{target.mention}'s Banner",
                timestamp=datetime.now().astimezone(),
            )
            .set_image(
                banner
            )
        )
        await ctx.respond(embed)
    else:
        await ctx.respond(
            "The user you specified doesn't have a banner set."
        )


@user_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member",
    description="The Discord member",
    type=hikari.User,
    required=False,
)
@lightbulb.command(
    name="avatar",
    aliases=["ava"],
    description="Displays the avatar of a Discord member or yours",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_avatar(ctx: lightbulb.Context) -> None:
    target = ctx.get_guild().get_member(ctx.options.member or ctx.user)

    if not target:
        await ctx.respond(
            "The user you specified isn't in the server.",
            delete_after=10,
        )
        return

    avatar = target.avatar_url or target.default_avatar_url
    if avatar:
        embed = (
            hikari.Embed(
                description=f"{target.mention}'s Avatar",
                timestamp=datetime.now().astimezone(),
            )
            .set_image(
                target.avatar_url or target.default_avatar_url
            )
        )
        await ctx.respond(embed)
    else:
        await ctx.respond(
            "The user you specified doesn't have an avatar set."
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(user_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(user_plugin)