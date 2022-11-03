import aiosqlite
import hikari
import lightbulb

greetings = lightbulb.Plugin("greetings")

"""
@greetings.listener(hikari.StartingEvent)
async def setup(_):
    async with aiosqlite.connect("memberlist.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (uid BIGINT);")
        await db.commit()


@greetings.listener(hikari.StartedEvent)
async def add_old_users(_):
    mems = greetings.cache.get_members_view_for_guild(993565814517141514)

    async with aiosqlite.connect("memberslist.db") as db:
        for m in mems.keys():
            exists = await (
                await db.execute("SELECT * FROM users WHERE uid = ?;", (m,))
            ).fetchone()
            if not exists:
                await db.execute("INSERT INTO users VALUES (?);", (m,))
        await db.commit()


@greetings.listener(hikari.MemberCreateEvent)
async def add_member(event: hikari.MemberCreateEvent):
    async with aiosqlite.connect("memberslist.db") as db:
        await db.execute("INSERT INTO users VALUES (?);", (id,))
"""


@greetings.listener(hikari.MemberCreateEvent)
async def on_member_join_update(event: hikari.MemberCreateEvent) -> None:
    before = event.old_member
    after = event.member
    role = 993695690578464778

    if role in [r.id for r in after.get_roles()] and role not in [
        r.id for r in before.get_roles()
    ]:
        await greetings.bot.rest.create_message(
            993567995936915536,
            f"You made it {after.mention}! Welcome to **{event.member.get_guild().name}**, enjoy your stay 💚",
            user_mentions=True,
        )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(greetings)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(greetings)
