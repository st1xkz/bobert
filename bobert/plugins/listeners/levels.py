import hikari
import lightbulb
from lightbulb.ext import tasks

levels = lightbulb.Plugin("levels")

# TODO find database hosting service or self host database and finish leveling system


async def calculate_xp_needed(level: int) -> int:
    # XP needed for each level
    level_reqs = {
        1: 5,
        2: 10,
        3: 25,
        4: 50,
        5: 100,
        6: 200,
        7: 500,
        8: 1000,
        9: 2000,
        10: 3000,
        11: 5000,
        12: 7000,
        13: 10000,
        14: 20000,
        15: 40000,
        16: 60000,
        17: 100000,
        18: 250000,
        19: 500000,
        20: 1000000000,
    }

    return level_reqs.get(level, 0)


"""
@tasks.task(m=2)
async def award_activity_xp() -> None:
    users = await levels.bot.d.levels_pool.fetch(
        "SELECT user_id, last_activity FROM bobert_levels"
    )

    for user in users:
        user_id, last_activity = user["user_id"], user["last_activity"]
        time_diff = (hikari.datetime.utcnow() - last_activity).total_seconds()

        if time_diff >= 120:
            await xp_gain(user_id)
"""


@levels.listener(hikari.GuildMessageCreateEvent)
async def level_up(event: hikari.GuildMessageCreateEvent) -> None:
    if event.guild_id == 993565814517141514:  # test server ID
        return

    user_id = event.message.author.id

    user_data = await levels.bot.d.levels_pool.fetchrow(
        "SELECT * FROM bobert_levels WHERE user_id = $1", user_id
    )
    if user_data is None:
        await levels.bot.d.levels_pool.execute(
            "INSERT INTO bobert_levels (user_id, xp, level, last_activity) VALUES ($1, 1, 1, CURRENT_TIMESTAMP)",
            user_id,
        )
    else:
        await levels.bot.d.levels_pool.execute(
            "UPDATE bobert_levels SET xp = xp + 1, last_activity = CURRENT_TIMESTAMP WHERE user_id = $1",
            user_id,
        )

        if (
            user_data["xp"] >= await calculate_xp_needed(user_data["level"])
            and user_data["level"] <= 20
        ):
            # Check if user leveled up
            new_level = await levels.bot.d.levels_pool.fetchval(
                "SELECT level FROM bobert_levels WHERE user_id = $1", user_id
            )

            await levels.bot.rest.create_message(
                1183975142532075601,
                f"Great job <@{user_id}>, you're now at level **{new_level}**!",
                user_mentions=True,
            )
            await levels.bot.d.levels_pool.execute(
                "UPDATE bobert_levels SET level = level + 1, xp = xp - $2 WHERE user_id = $1",
                user_id,
                await calculate_xp_needed(user_data["level"]),
            )


@levels.listener(hikari.MemberDeleteEvent)
async def delete_user(event: hikari.MemberDeleteEvent) -> None:
    if event.guild_id == 993565814517141514:  # test server ID
        return

    # Delete user from database when user is kicked, banned, or leaves the server
    user_id = event.user_id

    await levels.bot.d.levels_pool.execute(
        "DELETE FROM bobert_levels WHERE user_id = $1", user_id
    )


@levels.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member", description="the Discord member", type=hikari.Member, required=False
)
@lightbulb.command(
    name="rank",
    description="View your or another member's level and XP progress",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_rank(ctx: lightbulb.Context, member: hikari.Member) -> None:
    target = ctx.get_guild().get_member(member or ctx.user)

    user_data = await levels.bot.d.levels_pool.fetchrow(
        "SELECT * FROM bobert_levels WHERE user_id = $1", target.id
    )
    if user_data:
        await ctx.respond(
            f"{target.mention} is at level {user_data['level']} with {user_data['xp']} XP."
        )
    else:
        await ctx.respond(f"{target.mention} hasn't earned any XP!")


@levels.command
@lightbulb.command(name="reset-rank", description="Reset rank")
@lightbulb.implements(lightbulb.SlashCommand)
async def reset_rank(ctx: lightbulb.Context) -> None:
    await levels.bot.d.levels_pool.execute(
        "UPDATE bobert_levels SET level = 1, xp = 0 WHERE user_id = $1", ctx.author.id
    )
    await ctx.respond("Reset rank.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(levels)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(levels)
