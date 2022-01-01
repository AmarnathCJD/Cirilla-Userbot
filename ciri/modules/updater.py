import sys
from os import environ, execle, path, remove

import git
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from ciri.utils import asyncio, ciri_cmdimport

REPO_URL = "https://github.com/amarnathcjd/ciri-userbot.git"


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += (
            f"  • {c.summary} ({c.committed_datetime.strftime(d_form)}) <{c.author}>\n"
        )
    return ch_log


async def update_requirements():
    reqs = "requirements.txt"
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


async def update(event, repo, ups_rem, ac_br):
    try:
        ups_rem.pull(ac_br)
    except GitCommandError:
        repo.git.reset("--hard", "FETCH_HEAD")
    await update_requirements()
    await event.edit(
        "`Successfully Updated!\n" "Bot is restarting... Wait for a minute!`"
    )
    # Spin a new instance of bot
    args = [sys.executable, "-m", "userbot"]
    execle(sys.executable, *args, environ)
    return


@ciri_cmd(pattern="update")
async def update_ub(e):
    repo = git.Repo()
    try:
        repo.create_remote("upstream", REPO_URL)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ac_br = repo.active_branch.name
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if conf == "deploy":
        await event.edit("`Deploying userbot, please wait....`")
        return
    if changelog == "" and not force_update:
        await event.edit("\n`Ciri has no new updates with  " f"**master**\n")
        return repo.__del__()
    if conf == "" and not force_update:
        await e.edit(gen_changelog)
        await event.delete()
        return await event.respond(
            'do "[`.update now`] or [`.update deploy`]" to update.Check `.help updater` for details'
        )

    if force_update:
        await event.edit(
            "`Force-Syncing to latest stable userbot code, please wait...`"
        )
    if conf == "now":
        await event.edit("`Updating userbot, please wait....`")
        await update(event, repo, ups_rem, ac_br)
    return
