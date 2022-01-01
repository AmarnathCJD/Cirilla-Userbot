import asyncio
import os
from pathlib import Path

from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="spotdl", allow_sudo=True)
async def spot_dl(e):
    try:
        query = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await eor(e, "Song query was not provided.")
    cmd = "spotdl '{}'".format(query)
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    try:
        DIRECTORY = Path(".")
        file = DIRECTORY.glob("*.mp3")[0]
        print(file)
        await eor(e, "", file=file)
        os.remove(file)
    except Exception as ex:
        return await eor(e, str(ex))
    print(file)
