import asyncio
import io
import sys
import traceback

import requests

from ciri.utils import ciri_cmd, eor


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
        await e.respond(file=cmd)
        await e.delete()
    except Exception as c:
        await eor(e, str(c))


@ciri_cmd(pattern="goval")
async def go_eval(e):
    try:
        cmd = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await eor(e, "No cmd provided.")
    endpoint = "https://go.dev/_/compile"
    params = {"version": 2, "body": code, "withVet": True}
    with requests.post(endpoint, params=params).json() as resp:
        result = {"out": "nil", "err": "nil"}
        if resp.get("Events"):
            result["out"] = r["Events"][0]["Message"]
        if resp.get("Errors"):
            result["err"] = r["Errors"]
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
