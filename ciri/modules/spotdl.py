import asyncio
import os
import time
from pathlib import Path
from ciri import HelpStr

from ciri.core import progress
from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="spotdl", allow_sudo=True)
async def spot_dl(e):
    try:
        query = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await eor(e, "Song query was not provided.")
    cmd = "spotdl '{}'".format(query)
    await eor(e, "Processing ...")
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    try:
        file = list(Path(".").glob("*.mp3"))[0]
        await e.client.send_file(
            e.chat_id,
            file,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, e, time.time(), "Uploading...", file)
            ),
        )
        await e.delete()
        os.remove(file)
    except Exception as ex:
        await eor(e, "Song not found!")

HelpStr.append({
    "spotdl": {"description": "Downloads songs from spotify.", "usage": "spotdl <query>"},
})