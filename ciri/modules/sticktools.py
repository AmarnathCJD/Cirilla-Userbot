from ciri.utils import ciri_cmd, eor
import os

@ciri_cmd(pattern="stoi")
async def _stkr_to_img(e):
 r = await e.get_reply_message()
 if not r and not r.sticker:
    return await eor(e, "`Thats not a sticker.`")
 stk = await r.download_media()
 os.rename(skt, stk.replace('.webp', '.jpg'))
 await e.respond(file=stk.replace('.webp', '.jpg'))
 os.remove(stk.replace('.webp', '.jpg'))
