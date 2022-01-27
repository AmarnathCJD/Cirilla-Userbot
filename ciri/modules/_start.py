from ciri import ALIVE_PIC
from ciri.utils import ciri_cmd, eor
from telethon import types
ALIVE_PIC = []

ALIVE_CAPTION = """
<b>The Ciri Userbot...</b>

<b>Hey,  I am alive.</b>

<b>✵ Owner -</b> {}
<b>✵ Ultroid -</b> 0.1
<b>✵ UpTime -</b> soon!
<b>✵ Python -</b> <code>3.9.9</code>
<b>✵ Telethon -</b> </code>1.25.0</code>
<b>✵ Branch -</b>  <a href='github.com/amarnathcjd/cirilla-userbot'>master</a>
"""


@ciri_cmd(pattern="alive", allow_sudo=True)
async def _start(e):
    me = await e.client.get_me()
    image = None
    await e.delete()
    if len(ALIVE_PIC) == 1:
        image = ALIVE_PIC[0][1]
        if ALIVE_PIC[0][0] == "sticker":
            image = None
            await e.respond(file=ALIVE_PIC[0][1])
    await e.respond(
        ALIVE_CAPTION.format(me.first_name),
        file=image,
        parse_mode="html",
        link_preview=False,
    )


@ciri_cmd(pattern="setalivepic", allow_sudo=True)
async def set_dp(e):
    if not e.reply_to and not (await e.get_reply_message()).media:
        return await eor(e, "`Reply to image to set alive pic!`")
    r = await e.get_reply_message()
    if not r.photo and not r.sticker:
        return await eor(e, "Thats not a valid sticker or image.")
    if r.sticker:
        ALIVE_PIC.clear()
        ALIVE_PIC.append(
            [
                "sticker",
                types.Document(
                    id=r.document.id,
                    access_hash=r.document.access_hash,
                    file_reference=r.document.file_reference,
                ),
            ]
        )
    else:
        ALIVE_PIC.clear()
        ALIVE_PIC.append(
            [
                "photo",
                types.Photo(
                    id=r.photo.id,
                    access_hash=r.photo.access_hash,
                    file_reference=r.photo.file_reference,
                    sizes=r.photo.sizes,
                    attributes=[],
                    dc_id=r.photo.dc_id,
                ),
            ]
        )
    await eor(e, "sucessfully set custom alive pic.")
