import os

import asyncpg


async def init_db(pool):
    async with pool.acquire() as conn:
        with open("db/schema.sql", "r") as f:
            schema = f.read()
        await conn.execute(schema)


async def create_pool():
    return await asyncpg.create_pool(os.environ.get("PGSQL_TICKETS_URL"))
