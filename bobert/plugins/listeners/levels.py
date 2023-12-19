import hikari
import lightbulb
from lightbulb.ext import tasks

levels = lightbulb.Plugin("levels")


async def calculate_xp_needed(level: int) -> int:
    # Define XP needed for each level
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
        20: float("inf"),
    }

    return level_reqs.get(level, float("inf"))


async def xp_gain(user_id: int) -> None:
    user_data = await levels.bot.d.pool.fetchrow(
        "SELECT * FROM bobert_levels WHERE user_id = $1", user_id
    )
    if not user_data:
        await levels.bot.d.pool.execute(
            "INSERT INTO bobert_levels (user_id, xp, level, last_activity) VALUES ($1, 1, 1, CURRENT_TIMESTAMP)",
            user_id,
        )
    else:
        await levels.bot.d.pool.execute(
            "UPDATE bobert_levels SET xp = xp + 1, last_activity = CURRENT_TIMESTAMP WHERE user_id = $1",
            user_id,
        )

        while user_data["xp"] >= calculate_xp_needed(user_data["level"]):
            await levels.bot.d.pool.execute(
                "UPDATE bobert_levels SET level = level + 1, xp = xp - $2 WHERE user_id = $1",
                user_id,
                calculate_xp_needed(user_data["level"]),
            )

            # Check if user leveled up
            new_level = await levels.bot.d.pool.fetchval(
                "SELECT level FROM bobert_levels WHERE user_id = $1", user_id
            )
            if new_level > user_data["level"]:
                await levels.bot.rest.create_message(
                    993567969839960135,
                    f"Amazing job, <@{user_id}>! You're now at level {new_level}!",
                )


@tasks.task(m=2)
async def award_activity_xp() -> None:
    users = await levels.bot.d.pool.fetch(
        "SELECT user_id, last_activity FROM bobert_levels"
    )

    for user in users:
        user_id, last_activity = user["user_id"], user["last_activity"]
        time_diff = (hikari.datetime.utcnow() - last_activity).total_seconds()

        if time_diff >= 120:
            await xp_gain(user_id)


@levels.listener(hikari.MessageCreateEvent)
async def level_up(event: hikari.MessageCreateEvent) -> None:
    user_id = event.message.author.id
    await xp_gain(user_id)


@levels.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="member", description="the Discord member", type=hikari.Member, required=False
)
@lightbulb.command(
    name="rank", description="View your or another member's level and XP progress"
)
@lightbulb.implements(lightbulb.SlashCommand)
async def check_rank(ctx: lightbulb.Context) -> None:
    ...


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(levels)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(levels)
