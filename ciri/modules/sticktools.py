import os

from ciri import HelpStr
from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="stoi")
async def _stkr_to_img(e):
    r = await e.get_reply_message()
    if not r and not r.sticker:
        return await eor(e, "`Thats not a sticker.`")
    stk = await r.download_media()
    os.rename(stk, stk.replace(".webp", ".jpg"))
    await e.respond(file=stk.replace(".webp", ".jpg"))
    await e.delete()
    os.remove(stk.replace(".webp", ".jpg"))


@ciri_cmd(pattern="itos")
async def _kmg_to_stkr(e):
    r = await e.get_reply_message()
    if not r and not r.photo:
        return await eor(e, "`Thats not a image.`")
    pht = await r.download_media()
    new_name = pht.replace(pht.split(".")[-1], "") + ".jpg"
    os.rename(pht, new_name)
    await e.respond(file=new_name)
    await e.delete()
    os.remove(new_name)


HelpStr["stickertools"] = {
            "stoi": {"description": "Sticker to Image", "usage": ".stoi"},
            "itos": {"description": "Image to Sticker", "usage": ".itos"},
        }