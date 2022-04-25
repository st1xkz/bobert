import hikari
import lightbulb

from datetime import datetime


server_plugin = lightbulb.Plugin("server")


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="serverinfo",
    aliases=["server", "si"],
    description="Displays info about the server",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_server(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    ms = guild.get_members()
    cs = guild.get_channels()
    owner = await guild.fetch_owner()

    embed = (
        hikari.Embed(
            title=f"{guild.name}",
            description=f"""
            **ID**: {guild.id}
            **Owner**: {owner.username}#{owner.discriminator}
            **Description**: {guild.description}
            """,
            color=0x2f3136,
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Channels",
            f"""
            <:text:968015733026091038> {len([c for c in cs.values() if c.type == hikari.ChannelType.GUILD_TEXT])} ()
            <:voice:968015770527354930> {len([c for c in cs.values() if c.type == hikari.ChannelType.GUILD_VOICE])}
            """,
            inline=True,
        )
        .add_field(
            "Population",
            f"""
            Total: {len(ms)} ({len([m for m in ms.values() if not m.is_bot])} humans and {len([m for m in ms.values() if m.is_bot])} bots)
            """,
            inline=False,
        )
        .add_field(
            "Roles",
            f"{len(guild.get_roles())} roles",
            inline=False,
        )
        .add_field(
            "Creation Date",
            f"<t:{int(guild.created_at.timestamp())}:f>",
            inline=False,
        )
        .add_field(
            "Emoji",
            f"""
            Static:
            Animated:
            Total: {len(guild.get_emojis())}
            """,
            inline=True,
        )
        .add_field(
            "Verification Level",
            f"{guild.verification_level.name.title()}",
            inline=True,
        )
        .add_field(
            "Default Message Notifications",
            f"{guild.default_message_notifications.name.title()}",
            inline=True,
        )
        .add_field(
            "Explicit Content Filter",
            str(guild.explicit_content_filter).lower(),
            inline=True,
        )
        .add_field(
            "Boost Status",
            f"""
            Total: {guild.premium_subscription_count}
            Tier: {(guild.premium_tier) if guild.premium_tier else "0"}
            """,
            inline=False,
        )
        .set_thumbnail(
            guild.icon_url
        )
    )
    await ctx.respond(embed)


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.command(
    name="servericon",
    aliases=["sicon"],
    description="Displays the servers icon",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_servericon(ctx: lightbulb.Context) -> None:
    guild = ctx.bot.cache.get_guild(ctx.guild_id) or await ctx.bot.rest.fetch_guild(ctx.guild_id)
    embed = (
        hikari.Embed(
            title=f"Server Icon for {guild.name}",
            timestamp=datetime.now().astimezone(),
        )
        .set_image(
            guild.icon_url
        )
    )
    await ctx.respond(embed)


@server_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="The role to get the information from",
    type=hikari.Role,
    required=True,
)
@lightbulb.command(
    name="roleinfo",
    aliases=["role", "ri"],
    description="Displays info about a role",
)
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def cmd_role(ctx: lightbulb.Context) -> None:
    role = ctx.options.role
    ms = ctx.get_guild().get_members()

    role_created = int(role.created_at.timestamp())

    embed = (
        hikari.Embed(
            title=f"Role Info - {role.name}",
            color=role.color,
            description=f"ID: `{role.id}`",
            timestamp=datetime.now().astimezone(),
        )
        .add_field(
            "Administrator?",
            f"{bool(role.permissions & hikari.Permissions.ADMINISTRATOR)}",
            inline=True,
        )
        .add_field(
            "Mentionable?",
            f"{role.is_mentionable}",
            inline=True,
        )
        .add_field(
            "Color",
            f"{role.color.hex_code}",
            inline=True,
        )
        .add_field(
            "Role Position",
            f"{role.position}",
            inline=True,
        )
        .add_field(
            "Members",
            f"{len([m for m in  ms.values() if role.id in m.role_ids])}",
            inline=True,
        )
        .add_field(
            "Created At",
            f"<t:{role_created}:f> (<t:{role_created}:R>)",
            inline=False,
        )
        .set_footer(
            text=f"Requested by {ctx.member.username}#{ctx.member.discriminator}",
            icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
        )
    )
    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(server_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(server_plugin)