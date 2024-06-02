import ast
import asyncio
import contextlib
import io
import os
import re
import shutil
import sys
import textwrap
import time
import traceback
from datetime import datetime
from typing import Final, Mapping, Pattern

import aiohttp
import hikari
import lightbulb

eval = lightbulb.Plugin("eval")
eval.add_checks(lightbulb.checks.owner_only)

DEFAULT_SHELL = os.getenv(
    "SHELL", "cmd" if os.name in ("win32", "win64", "winnt", "nt") else "bash"
)
CODEBLOCK_PATTERN: Final[Pattern[str]] = re.compile(
    r"```(?P<language>[a-zA-Z0-9]*)\s(?P<content>[\s\S]*?)\s*```"
)
LANGUAGES: Final[Mapping[str, str]] = {
    "": "python",
    "py": "python",
    "python": "python",
    "python3": "python",
    "py3": "python",
    "shell": DEFAULT_SHELL,
    "sh": DEFAULT_SHELL,
    "bash": DEFAULT_SHELL,
}


async def execute_in_session(ctx: lightbulb.context.Context, code: str):
    sout = io.StringIO()
    serr = io.StringIO()

    with contextlib.redirect_stdout(sout):
        with contextlib.redirect_stderr(serr):
            start_time = time.monotonic()
            try:
                try:
                    abstract_syntax_tree = ast.parse(code)
                    if isinstance(abstract_syntax_tree.body[0], ast.Expr):
                        code = f"return {code.strip()}"
                except Exception:
                    pass

                exec_globals = {}
                exec_locals = {"ctx": ctx, "bot": ctx.bot}

                func_code = (
                    f"async def _aexec(ctx, bot):\n{textwrap.indent(code, '    ')}"
                )
                exec(func_code, exec_globals, exec_locals)

                _aexec = exec_locals["_aexec"]

                start_time = time.monotonic()
                result = await _aexec(ctx, ctx.bot)
                if hasattr(result, "__await__"):
                    print(f"Returned awaitable {result}. Awaiting it.", file=sys.stderr)
                    result = await result
            except BaseException as ex:
                traceback.print_exc()
                result = type(ex)
            finally:
                exec_time = time.monotonic() - start_time

    return (
        sout.getvalue(),
        serr.getvalue(),
        result,
        exec_time,
        f'Python {sys.version.replace(chr(10), " ")}',
    )


async def execute_in_shell(_: lightbulb.context.Context, command: str, script: str):
    command_path = shutil.which(command)
    if not command_path:
        return "", f"{command} not found.", 127, 0.0, ""

    start_time = time.monotonic()
    process = await asyncio.create_subprocess_exec(
        command_path,
        "--",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate(script.encode("utf-8"))
    execution_time = time.monotonic() - start_time

    stdout = stdout.decode()
    stderr = stderr.decode()

    return stdout, stderr, str(process.returncode), execution_time, command_path


async def fetch_paste_content(paste_id: str):
    url = f"https://api.pastes.dev/{paste_id}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
        except aiohttp.ClientError:
            return None


@eval.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="code",
    description="Code to evaluate",
    type=str,
    modifier=lightbulb.OptionModifier.CONSUME_REST,
)
@lightbulb.command(
    name="eval",
    description="Evaluates the given python or shell code",
    pass_options=True,
    hidden=True,
)
@lightbulb.implements(lightbulb.PrefixCommand)
async def eval_command(ctx: lightbulb.context.Context, code: str):
    """Evaluates the given python or shell code either as a code block or from a paste URL. Only one website is supported: https://pastes.dev/"""
    if code.startswith("https://pastes.dev/"):
        paste_id = code.split("/")[-1]
        paste_content = await fetch_paste_content(paste_id)
        if paste_content is None:
            await ctx.respond(
                "❌ Failed to fetch paste content. Please make sure the paste ID is correct and try again.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return
        code = paste_content

    if code.startswith("```"):
        match = CODEBLOCK_PATTERN.match(code)
        if not match:
            await ctx.respond(
                "❌ No code block found in the provided input.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return
        language = match.group("language")
        code_content = match.group("content").strip()
    else:
        language = "shell" if ctx.invoked_with in ["shell", "sh"] else "python"
        code_content = code

    lang = LANGUAGES.get(language, language)

    executor = execute_in_session if lang == "python" else execute_in_shell

    stdout, stderr, result, exec_time, prog = await executor(ctx, code_content)

    info = f"-------- Python {sys.version.split(' ')[0]} ({sys.version_info[3].split()[0]}, {datetime.now().strftime('%b %d, %Y @ %H:%M')}) ----"
    value_ms = f"Time taken: {exec_time * 1000:.2f}ms"

    if stderr:
        content = f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\n\u001b[0;31m{stderr.rstrip()}\u001b[0;0m\n\u001b[0;34m{value_ms}\u001b[0;0m\n```"
    else:
        content = f"```ansi\n\u001b[0;37m{info}\u001b[0;0m\n\u001b[0;32m{stdout.rstrip()}\u001b[0;0m\n\u001b[0;34m{value_ms}\u001b[0;0m\n```"

    await ctx.respond(content)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(eval)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(eval)
