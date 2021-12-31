from bing_image_urls import bing_image_urls as image_dl
from telethon import functions
import asyncio
from ciri.utils import ciri_cmd, eor

AUTO_DP = False
PICS = []
import io
import logging

from requests import get


@ciri_cmd(pattern="autodp", allow_sudo=True)
async def _auto_dp(e):
    global AUTO_DP, PICS
    try:
        args = e.text.split(maxsplit=1)[1]
    except IndexError:
        await eor(e, "give some query for autodp.")
    if args == "off":
        AUTO_DP = False
        await eor(e, "AutoDP has been disabled.")
        return
    search = image_dl(args, limit=80)
    if search == None:
        return await eor(e, "No results found for search '{}'.".format(args))
    PICS = search
    await eor(e, "AutoDP has been started with keyword '{}'.".format(args))
    chance = -1
    AUTO_DP = True
    while AUTO_DP and len(PICS) > chance + 1:
        try:
            chance += 1
            file_fetch = get(PICS[chance]).content
            with io.BytesIO(file_fetch.content) as b:
                b.name = "wall.jpg"
                file = await e.client.upload_file(b)
            await e.client(functions.photos.UploadProfilePhotoRequest(file))
        except Exception as exception:
            logging.info(exception)
        await asyncio.sleep(60)
