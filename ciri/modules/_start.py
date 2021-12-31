from telethon import types

from ciri import ALIVE_PIC
from ciri.utils import ciri_cmd, eor

if not ALIVE_PIC:
    ALIVE_PIC = types.Document(
        id=6068927430792315582,
        access_hash=-2620307863328118732,
        file_reference=b"\x02H\xdeIR\x00\x04\xd5Oa\xcf3O\x8f\xe4\xefc\x97\\a\xea\x15\xeb\x86yG\xa0U\x19",
        date=datetime.datetime(2021, 4, 26, 5, 41, 13, tzinfo=datetime.timezone.utc),
        mime_type="image/webp",
        size=9064,
        dc_id=5,
        attributes=[],
    )


@ciri_cmd(pattern="alive")
async def _start(e):
    ALIVE_TEXT = "Ciri is Ready to Rock\n\nSystem Status\n**••Mу Bσѕѕ••** : {}\n**тєℓєтнσи νєяѕισи** : {}\nLι¢єиѕє: [ӀíϲҽղՏҽ](https://github.com/amarnathcjd/ciri-userbot/blob/master/LICENSE)\n"
    me = await e.client.get_me()
    await eor(e, ALIVE_TEXT.format(me.first_name, "1.24"), "md", False)
