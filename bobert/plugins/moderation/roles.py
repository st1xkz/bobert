import hikari
import lightbulb

roles = lightbulb.Plugin("role")
roles.add_checks(
    lightbulb.checks.has_guild_permissions(hikari.Permissions.MANAGE_ROLES)
)


@roles.command
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
    name="create-role",
    description="Creates a role",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def create_role(ctx: lightbulb.Context, role_name: str, role_color: str) -> None:
    role = await ctx.bot.rest.create_role(
        ctx.get_guild(),
        name=role_name,
        color=int(role_color, 16) if role_color else None,
    )
    await ctx.respond(f"Role {role.mention} has been created by `{ctx.user}`")


@roles.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="role",
    description="the role to delete",
    type=hikari.Role,
    required=True,
)
@lightbulb.command(
    name="delete-role",
    description="Deletes a role",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def delete_role(ctx: lightbulb.Context, role: hikari.Role) -> None:
    await ctx.bot.rest.delete_role(ctx.guild_id, role.id)
    await ctx.respond(f"Role `{role}` has been deleted by `{ctx.user}`")


@roles.command
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
    name="give-role",
    description="Gives a role to the specified user",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def give_role(ctx: lightbulb.Context, member: hikari.Member, role: hikari.Role) -> None:
    if _role in member.get_roles():
        await ctx.respond("The user you specified already has that role.")

    else:
        await member.add_role(role)
        await ctx.respond(f"👍 Role {role.mention} has been added to {member.mention} by **{ctx.user}**")


@roles.command
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
    name="remove-role",
    description="Removes a role from the specified user",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def remove_role(ctx: lightbulb.Context, member: hikari.Member, role: hikari.Role) -> None:
    if _role not in member.get_roles():
        await ctx.respond(
            "That role has already been removed from the specified user or they never had it to begin with."
        )

    else:
        await member.remove_role(role)
        await ctx.respond(f"👍 Role {role.mention} has been removed from {member.mention} by **{ctx.user}**")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(roles)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(roles)
