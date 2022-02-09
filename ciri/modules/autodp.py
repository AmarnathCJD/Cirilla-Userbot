import asyncio

from bing_image_urls import bing_image_urls as image_dl
from telethon import functions

from ciri.utils import ciri_cmd, eor

AUTO_DP = False
QUERY = ""
PICS = []
import io
import logging

from requests import get


@ciri_cmd(pattern="autodp", allow_sudo=True)
async def _auto_dp(e):
    try:
        args = e.text.split(maxsplit=1)[1]
    except IndexError:
        if not QUERY:
            await eor(e, "give some query for autodp.")
        else:
            await eor(e, "autodp is running with `{}`".format(QUERY))
    if args == "off":
        AUTO_DP = False
        await eor(e, "AutoDP has been disabled.")
        PICS.clear()
        return
    search = image_dl(args, limit=80)
    if search == None:
        return await eor(e, "No results found for search '{}'.".format(args))
    PICS.clear()
    for x in search:
        PICS.append(x)
    await eor(e, "AutoDP has been started with keyword '{}'💗.".format(args))
    AUTO_DP = True
    QUERY = args
    chance = 0
    print(AUTO_DP, len(PICS))
    while AUTO_DP and len(PICS) != 0 and QUERY == args:
        try:
            file_fetch = get(PICS[chance]).content
            with io.BytesIO(file_fetch) as b:
                b.name = "pic.jpg"
                file = await e.client.upload_file(b)
            PICS.pop(chance)
            chance += 1
            await e.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as exception:
            logging.info(exception)
        await asyncio.sleep(60)


@ciri_cmd(pattern="setdp")
async def set_dp(e):
    r = await e.get_reply_message()
    if not r and not r.photo and not r.video:
        await eor(e, "Reply to an image/video to set dp.")
    else:
        try:
            if r.photo:
                await e.client(functions.photos.UploadProfilePhotoRequest(file=r.photo))
            elif r.video:
                await e.client(functions.photos.UploadProfilePhotoRequest(video=r.video))
        except Exception as c:
            await eor(e, str(c))
            return
    await eor(e, "done.")
