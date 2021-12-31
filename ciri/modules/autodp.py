from bing_image_urls import bing_image_urls as image_dl
from telethon import functions

from ciri.utils import ciri_cmd, eor

AUTO_DP = False
PICS = []
import io
import logging

from requests import get


@ciri_cmd("autodp", allow_sudo=True)
async def _auto_dp(e):
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
    while AUTO_DP and len(PICS) != 0:
        try:
            chance += 1
            if chance != 0:
                dp = await e.client.get_profile_photos("me", limit=1)
                await e.client(functions.photos.DeletePhotosRequest(dp))
            file_fetch = get(PICS[chance]).content
            with io.BytesIO(file_fetch.content) as b:
                b.name = "wall.jpg"
                file = await e.client.upload_file(b)
            await e.client(functions.photos.UploadProfilePhotoRequest(file))
            await asyncio.sleep(60)
        except Exception as exception:
            logging.info(exception)
