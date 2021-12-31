from ciri import ALIVE_PIC
from ciri.utils import ciri_cmd, eor

if not ALIVE_PIC:
    ALIVE_PIC = "https://te.legra.ph/file/f5fd85a59ab9284b2ef83.jpg"


@ciri_cmd(pattern="alive", allow_sudo=True)
async def _start(e):
    ALIVE_TEXT = "<b>Eliza</b> is Ready to Rock\n\nSystem Status\n<b>••Mу Bσѕѕ••</b> : {}\n<b>тєℓєтнσи νєяѕισи</b> : {}\nLι¢єиѕє: <b><a href='https://github.com/amarnathcjd/ciri-userbot/blob/master/LICENSE'>ӀíϲҽղՏҽ</a></b>\n"
    me = await e.client.get_me()
    await eor(
        e=e,
        msg=ALIVE_TEXT.format(me.first_name, "1.24"),
        file=ALIVE_PIC,
        parse_mode="htm",
        link_preview=False,
    )

@ciri_cmd(pattern="spoil", allow_sudo)
async def _spoil_text(e):
 try:
   TEX = e.text.split(maxsplit=1)[1]
 except IndexError:
   return await eor(e, "give text to spoil!")
 await eor(e, "<span class='tg-spoiler'>" + TEX + "</span>?", None, "html", False)
