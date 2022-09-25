import hikari
import lightbulb

role_plugin = lightbulb.Plugin("role")
role_plugin.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_ROLES)
)


@role_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role_color",
    description="the color of the role",
    required=False,
)
@lightbulb.option(
    name="role_name",
    description="the name of the role",
    required=False,
    default="new role",
)
@lightbulb.command(
    name="createrole",
    description="Creates a role",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_create_role(ctx: lightbulb.Context) -> None:
    role = await ctx.bot.rest.create_role(
        ctx.get_guild(),
        name=ctx.options.role_name,
        color=int(ctx.options.role_color, 16) if ctx.options.role_color else None,
    )
    await ctx.respond(f"Role {role.mention} has been created by `{ctx.user}`")


@role_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to delete",
    type=hikari.Role,
    required=True,
)
@lightbulb.command(
    name="deleterole",
    description="Deletes a role",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_delete_role(ctx: lightbulb.Context) -> None:
    await ctx.bot.rest.delete_role(ctx.guild_id, ctx.options.role.id)
    await ctx.respond(f"Role `{ctx.options.role}` has been deleted by `{ctx.user}`")


@role_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to give",
    type=hikari.Role,
    required=True,
)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="giverole",
    description="Gives a role to the specified user",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_give_role(ctx: lightbulb.Context) -> None:
    if ctx.options.role in ctx.options.member.get_roles():
        await ctx.respond("The user you specified already has that role.")

    else:
        await ctx.options.member.add_role(ctx.options.role)
        embed = hikari.Embed(
            description=f"<:yes:993687377841234022> Role {ctx.options.role.mention} has been added to {ctx.options.member.mention} by **{ctx.user}**",
            color=0x2F3136,
        )
        await ctx.respond(embed=embed)


@role_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to remove",
    type=hikari.Role,
    required=True,
)
@lightbulb.option(
    name="member",
    description="the Discord member",
    type=hikari.Member,
    required=True,
)
@lightbulb.command(
    name="removerole",
    description="Removes a role from the specified user",
)
@lightbulb.implements(lightbulb.SlashCommand)
async def cmd_remove_role(ctx: lightbulb.Context) -> None:
    if ctx.options.role not in ctx.options.member.get_roles():
        await ctx.respond(
            "That role has already been removed from the specified user or they never had it to begin with."
        )

    else:
        await ctx.options.member.remove_role(ctx.options.role)
        embed = hikari.Embed(
            description=f"<:yes:993687377841234022> Role {ctx.options.role.mention} has been removed from {ctx.options.member.mention} by **{ctx.user}**",
            color=0x2F3136,
        )
        await ctx.respond(embed=embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(role_plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(role_plugin)
