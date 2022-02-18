import asyncio
from os import system

import aria2p

from ciri.utils import ciri_cmd

cmd = "aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port 6800  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"
aria2 = aria2p.API(aria2p.Client(host="http://localhost", port=6800, secret=""))

TIME_OUT = 5


aria2_is_running = system(cmd)


@ciri_cmd(pattern="mg")
async def _dl_torrent(e):
    t = e.text.split(" ", maxsplit=1)
    if len(t) == 1:
        return await e.reply("k")
    t = t[1]
    urls = [t]
    try:
        download = aria2.add_uris(urls, options=None, position=None)
    except Exception as e:
        return await eor(e, "`Error:\n`" + str(e))
    gid = download.gid
    complete = None
    file = aria2.get_download(gid)
    if file.followed_by_ids:
        new_gid = await check_metadata(gid)
        await progress_status(gid=new_gid, event=e, previous=None)
    while complete != True:
        file = aria2.get_download(gid)
        complete = file.is_complete
        try:
            msg = (
                "**Downloading File:** "
                + str(file.name)
                + "\n**Speed:** "
                + str(file.download_speed_string())
                + "\n**Progress:** "
                + str(file.progress_string())
                + "\n**Total Size:** "
                + str(file.total_length_string())
                + "\n**ETA:**  "
                + str(file.eta_string())
                + "\n\n"
            )
            await e.edit(msg)
            await asyncio.sleep(TIME_OUT)
        except Exception:
            pass

    await e.edit("**File Downloaded Successfully:** `{}`".format(file.name))


async def progress_status(gid, event, previous):
    try:
        file = aria2.get_download(gid)
        if not file.is_complete:
            if not file.error_message:
                msg = (
                    "Downloading File: `"
                    + str(file.name)
                    + "`\nSpeed: "
                    + str(file.download_speed_string())
                    + "\nProgress: "
                    + str(file.progress_string())
                    + "\nTotal Size: "
                    + str(file.total_length_string())
                    + "\nStatus: "
                    + str(file.status)
                    + "\nETA:  "
                    + str(file.eta_string())
                    + "\n\n"
                )
                if previous != msg:
                    await event.edit(msg)
                    previous = msg
            else:
                logger.info(str(file.error_message))
                await event.edit("Error : `{}`".format(str(file.error_message)))
                return
            await asyncio.sleep(TIME_OUT)
            await progress_status(gid, event, previous)
        else:
            await event.edit("File Downloaded Successfully: `{}`".format(file.name))
            return
    except Exception as e:
        if " not found" in str(e) or "'file'" in str(e):
            await event.edit("Download Canceled :\n`{}`".format(file.name))
            return
        elif " depth exceeded" in str(e):
            file.remove(force=True)
            await event.edit(
                "Download Auto Canceled :\n`{}`\nYour Torrent/Link is Dead.".format(
                    file.name
                )
            )
        else:
            logger.info(str(e))
            await event.edit("Error :\n`{}`".format(str(e)))
            return


async def check_metadata(gid):
    file = aria2.get_download(gid)
    new_gid = file.followed_by_ids[0]
    return new_gid
