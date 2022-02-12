import datetime

from telethon import types

from ciri import ALIVE_PIC
from ciri.utils import ciri_cmd, eor

from .db import get_dp, set_dp

ALIVE_PIC = []

ALIVE_CAPTION = """
<b>The Ciri Userbot...</b>

<b>Hey,  I am alive.</b>

<b>✵ Owner -</b> {}
<b>✵ Ciri -</b> v1.2
<b>✵ UpTime -</b> soon!
<b>✵ Python -</b> <code>3.10</code>
<b>✵ Telethon -</b> </code>1.25.1</code>
<b>✵ Branch -</b>  <a href='github.com/amarnathcjd/cirilla-userbot'>master</a>
"""


@ciri_cmd(pattern="alive", allow_sudo=True)
async def _start(e):
    me = await e.client.get_me()
    await e.delete()
    await e.respond(
        ALIVE_CAPTION.format(me.first_name),
        file=construct_dp(),
        parse_mode="html",
        link_preview=False,
    )


@ciri_cmd(pattern="setalivepic", allow_sudo=True)
async def set_dp(e):
    payload = e.text.split()
    if len(payload) > 1:
        payload = payload[1]
    else:
        payload = ""
    if not payload:
        if not e.reply_to and not (await e.get_reply_message()).media:
            return await eor(e, "`Reply to image to set alive pic!`")
        r = await e.get_reply_message()
        if not r.photo and not r.sticker:
            return await eor(e, "Thats not a valid sticker or image.")
        if r.sticker:
            _type = "document"
            _id = r.sticker.id
            _access_hash = r.sticker.access_hash
            _file_reference = r.sticker.file_reference
        elif r.photo:
            _type = "photo"
            _id = r.photo.id
            _access_hash = r.photo.access_hash
            _file_reference = r.photo.file_reference
    else:
        _type = "link"
        _id = payload
        _access_hash = ""
        _file_reference = ""
    set_dp(_id, _access_hash, _file_reference, _type)
    await eor(e, "sucessfully set custom alive pic.")


@ciri_cmd(pattern="ping")
async def _ping(e):
    s = datetime.datetime.now()
    r = await eor(e, "`Pinging...`")
    f = datetime.datetime.now() - s
    await r.edit(
        "Pong!\n<code>{}</code>".format(str(f.microseconds)[:3] + " ms"),
        parse_mode="html",
    )


def construct_dp():
    dp = get_dp()
    if not dp:
        return nil
    if dp["type"] == "link":
        return dp["id"]
    elif dp["type"] == "sticker":
        return types.Document(
            id=dp["id"],
            access_hash=dp["access_hash"],
            file_reference=dp["file_reference"],
        )
    elif dp["type"] == "photo":
        return types.Photo(
            id=dp["id"],
            access_hash=dp["access_hash"],
            file_reference=dp["file_reference"],
            dc_id=4,
            date=datetime.datetime.now(),
            sizes=[6],
        )
