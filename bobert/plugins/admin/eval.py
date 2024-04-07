import ast
import contextlib
import io
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime

import aiohttp
import hikari
import lightbulb

eval = lightbulb.Plugin("eval")
eval.add_checks(lightbulb.checks.owner_only)


async def fetch_paste_content(paste_id):
    url = f"https://api.pastes.dev/{paste_id}"
    async with aiohttp.ClientSession() as sess:
        try:
            async with sess.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    return None
        except aiohttp.ClientError as err:
            return None


@eval.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="url",
    description="The paste URL containing the code (https://pastes.dev/)",
    type=str,
)
@lightbulb.command(
    name="eval",
    description="Evaluates code from a paste URL",
    pass_options=True,
    hidden=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def eval_command(ctx: lightbulb.Context, url: str) -> None:
    """Evaluates code from a paste URL. Only one website is supported: https://pastes.dev/"""
    paste_id = url.split("/")[-1]

    # Fetch paste content from pastes.dev
    paste_content = await fetch_paste_content(paste_id)
    if paste_content is None:
        await ctx.respond(
            "❌ Failed to fetch paste content. Please make sure the paste ID is correct and try again.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    renv = {
        "author": ctx.author,
        "_bot": ctx.bot,
        "_app": ctx.app,
        "_channel": ctx.get_channel(),
        "_guild": ctx.get_guild(),
        "_message": paste_content,
        "_ctx": ctx,
        "subprocess": subprocess,
    }

    _fn_name = "__bobert_eval"
    code = "\n".join(f"     {i}" for i in paste_content.strip().splitlines())
    stdout, stderr = io.StringIO(), io.StringIO()
    start_time = time.time()

    try:
        parsed: ast.Module = ast.parse(f"async def {_fn_name}():\n{code}")
        body = parsed.body[0].body
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # Insert returns into the body and the orelse for if statements
        if isinstance(body[-1], ast.If):

            def add_returns(body: list) -> None:
                for node in body:
                    if isinstance(node, ast.Expr):
                        ast.fix_missing_locations(node)
                    elif isinstance(node, ast.If):
                        add_returns(node.body)
                        add_returns(node.orelse)
                    elif isinstance(node, ast.With):
                        add_returns(node.body)

            add_returns(body)

        exec(compile(parsed, filename="<ast>", mode="exec"), renv)
        fn = renv[_fn_name]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            await fn()
    except Exception as e:
        stderr.write(f"{type(e).__name__}: {e}\n")
        traceback.print_exc(file=stderr)
    finally:
        end_time = time.time()
        exec_time_ms = round((end_time - start_time) * 1000, 2)

    stdout = stdout.getvalue()
    stderr = stderr.getvalue()

    info = f"---- Python {sys.version.split(' ')[0]} ({sys.version_info[3].split()[0]}, {datetime.now().strftime('%b %d, %Y @ %H:%M')}) ----\n"
    value_ms = f"Time taken: {exec_time_ms}ms"

    if stderr:
        await ctx.respond(
            f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\u001b[0;31m{stderr}\u001b[0;0m\u001b[0;34m{value_ms}\u001b[0;0m\n```"
        )
    else:
        await ctx.respond(
            f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\u001b[0;32m{stdout}\u001b[0;0m\u001b[0;34m{value_ms}\u001b[0;0m\n```"
        )


"""
@eval.listener(hikari.MessageCreateEvent)
async def mention_eval(event: hikari.MessageCreateEvent) -> None:
    bot = event.message.app

    # Check if bot is mentioned in message content and if "eval" is in content
    if (
        bot is not None
        and bot.get_me() is not None
        and bot.get_me().mention in event.message.content
    ):
        code = event.message.content.split("`")
        renv = {
            "author": event.author,
            "_bot": event.bot,
            "_app": event.app,
            "_channel": event.get_channel(),
            "_guild": event.get_guild(),
            "_message": code,
            "_ctx": None,
            "subprocess": subprocess,
        }

    _fn_name = "__bobert_eval"
    code = "\n".join(f"     {i}" for i in code.strip().splitlines())
    stdout, stderr = io.StringIO(), io.StringIO()
    start_time = time.time()

    try:
        parsed: ast.Module = ast.parse(f"async def {_fn_name}():\n{code}")
        body = parsed.body[0].body
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # Insert returns into the body and the orelse for if statements
        if isinstance(body[-1], ast.If):

            def add_returns(body: list) -> None:
                for node in body:
                    if isinstance(node, ast.Expr):
                        ast.fix_missing_locations(node)
                    elif isinstance(node, ast.If):
                        add_returns(node.body)
                        add_returns(node.orelse)
                    elif isinstance(node, ast.With):
                        add_returns(node.body)

            add_returns(body)

        exec(compile(parsed, filename="<ast>", mode="exec"), renv)
        fn = renv[_fn_name]
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            await fn()
    except Exception as e:
        stderr.write(f"{type(e).__name__}: {e}\n")
        traceback.print_exc(file=stderr)
    finally:
        end_time = time.time()
        exec_time_ms = round((end_time - start_time) * 1000, 2)

    stdout = stdout.getvalue()
    stderr = stderr.getvalue()

    info = f"---- Python {sys.version.split(' ')[0]} ({sys.version_info[3].split()[0]}, {datetime.now().strftime('%b %d, %Y @ %H:%M')}) ----\n"
    value_ms = f"Time taken: {exec_time_ms}ms"

    if stderr:
        await event.respond(
            f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\u001b[0;31m{stderr}\u001b[0;0m\u001b[0;34m{value_ms}\u001b[0;0m\n```"
        )
    else:
        await event.respond(
            f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\u001b[0;32m{stdout}\u001b[0;0m\u001b[0;34m{value_ms}\u001b[0;0m\n```"
        )
"""


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(eval)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(eval)
