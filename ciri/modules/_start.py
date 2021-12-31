from telethon import types
import datetime
from ciri import ALIVE_PIC
from ciri.utils import ciri_cmd, eor

if not ALIVE_PIC:
    ALIVE_PIC = "https://te.legra.ph/file/f5fd85a59ab9284b2ef83.jpg"


@ciri_cmd(pattern="alive")
async def _start(e):
    ALIVE_TEXT = "Eliza is Ready to Rock\n\nSystem Status\n**••Mу Bσѕѕ••** : {}\n**тєℓєтнσи νєяѕισи** : {}\nLι¢єиѕє: [ӀíϲҽղՏҽ](https://github.com/amarnathcjd/ciri-userbot/blob/master/LICENSE)\n"
    me = await e.client.get_me()
    await eor(e, ALIVE_TEXT.format(me.first_name, "1.24"), "md", False)
