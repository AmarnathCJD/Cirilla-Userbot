import asyncio
import io
import os
import sys
import traceback

import requests

from ciri import THUMB_FILE, HelpStr
from ciri.utils import ciri_cmd, eor, errors


@ciri_cmd(pattern="eval", full_sudo=True)
async def eval__(e):
    try:
        a = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await e.edit("`Give some python cmd`")
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    ros = sys.stdout = io.StringIO()
    red = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(a, e)
    except Exception:
        exc = traceback.format_exc()
    stdout = ros.getvalue()
    stderr = red.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = (
        "__►__ **EVALPy**\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
            a,
            evaluation,
        )
    )
    if len(evaluation) > 4095:
        with io.BytesIO(evaluation.encode()) as finale_b:
            finale_b.name = "eval.txt"
            return await eor(e, f"```{a}```", file=finale_b)
    await eor(e, final_output)


async def aexec(code, event):
    exec(
        f"async def __aexec(e, client): "
        + "\n message = event = e"
        + "\n reply = await event.get_reply_message()"
        + "\n p = print"
        + "".join(f"\n {l}" for l in code.split("\n")),
    )

    return await locals()["__aexec"](event, event.client)


@ciri_cmd(pattern="(bash|exec)", full_sudo=True)
async def __exec(e):
    try:
        cmd = e.text.split(maxsplit=1)[1]
    except IndexError:
        return
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    result = str(stdout.decode().strip()) + str(stderr.decode().strip())
    cresult = f"<b>Bash:~#</b> <code>{cmd}</code>\n<b>Result:</b> <code>{result}</code>"
    if len(result) > 4095:
        with io.BytesIO(result.encode()) as file:
            file.name = "bash.txt"
            await e.respond(f"<code>{cmd}</code>", file=file, parse_mode="html")
            return await e.delete()
    await eor(e, cresult, parse_mode="html")


@ciri_cmd(pattern="ul")
async def upload(e):
    try:
        cmd = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await eor(e, "Provide the path to file!")
    try:
        await e.respond(file=cmd, thumb=THUMB_FILE)
        await e.delete()
    except Exception as c:
        await eor(e, str(c))


@ciri_cmd(pattern="goval", allow_sudo=True)
async def go_eval(e):
    try:
        cmd = e.text.split(maxsplit=1)[1]
    except IndexError:
        await eor(e, "No cmd provided.")
        return
    endpoint = "https://go.dev/_/compile"
    print(1)
    params = {"version": 2, "body": cmd, "withVet": True}
    print(2)
    r = requests.post(endpoint, params=params)
    resp = r.json()
    print(3)
    print(resp)
    result = {"out": "nil", "err": "nil"}
    if resp.get("Events"):
        result["out"] = resp["Events"][0]["Message"]
    if resp.get("Errors"):
        result["err"] = resp["Errors"]
    if result["out"] != "nil":
        evaluation = result["out"]
    elif result["err"] != "nil":
        evaluation = result["err"]
    else:
        evaluation = "nil"
    final_output = (
        "__►__ **EVALGo**\n```{}``` \n\n __►__ **OUTPUT**: \n```{}``` \n".format(
            cmd,
            evaluation,
        )
    )
    await eor(e, final_output)


@ciri_cmd(pattern="ls")
async def _ls(e):
    try:
        cmd = e.text.split(maxsplit=1)[1]
    except IndexError:
        cmd = "."
    try:
        Files = os.listdir(cmd)
    except BaseException as b:
        return await eor(e, str(b))
    Dir = "**Directory Manager** \n"
    for D in Files:
        if os.path.isdir(cmd + "/" + D):
            Dir += "📁 " + D + "\n"
        else:
            if D.endswith(("jpg", "png", "webp")):
                Dir += "📸 " + D + "\n"
            elif D.endswith(("mp4", "mkv", "webm")):
                Dir += "🎞 " + D + "\n"
            elif D.endswith(("mp3", "m4a", "mpeg")):
                Dir += "📀 " + D + "\n"
            elif D.endswith(("txt", "doc", "csv", "json")):
                Dir += "📝 " + D + "\n"
            elif D.endswith("torrent"):
                Dir += "🌀 " + D + "\n"
            else:
                Dir += "❔ " + D + "\n"
    await eor(e, Dir)


@ciri_cmd(pattern="err")
async def see_last_exception(e):
    await eor(e, "**Latest Exception**:\n" + str(errors["latest"]))

HelpStr.append({
    "eval": {"description": "Evaluate a code", "usage": "eval <code>"},
    "exec": {"description": "Execute a code", "usage": "exec <code>"},
    "goval": {"description": "Evaluate a code in go", "usage": "goeval <code>"},
    "ls": {"description": "List files in a directory", "usage": "ls <directory>"},
    "ul": {"description": "Upload a file", "usage": "ul <file>"},
})