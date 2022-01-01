import asyncio
import os
import time
from pathlib import Path

from ciri.core import progress
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
        file = list(Path(".").glob("*.mp3"))[0]
        await eor(e, "Processing ...")
        await e.client.send_file(
            e.chat_id,
            file,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, e, time.time(), "Uploading...", file)
            ),
        )
        await e.respond("", file=file)
        os.remove(file)
    except Exception as ex:
        return await eor(e, str(ex))
    print(file)
