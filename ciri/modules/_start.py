from ciri import ALIVE_PIC, bot as xbot
from ciri.utils import ciri_cmd, eor

if not ALIVE_PIC:
    ALIVE_PIC = "https://te.legra.ph/file/f5fd85a59ab9284b2ef83.jpg"


@ciri_cmd(pattern="alive", allow_sudo=True)
async def _start(e):
    ALIVE_TEXT = "<b>Eliza</b> is Ready to Rock\n\nSystem Status\n<b>••Mу Bσѕѕ••</b> : {}\n<b>тєℓєтнσи νєяѕισи</b> : {}\nLι¢єиѕє: <b><a href='https://github.com/amarnathcjd/ciri-userbot/blob/master/LICENSE'>ӀíϲҽղՏҽ</a></b>\n"
    me = await e.client.get_me()
    await e.delete()
    await e.respond(
        ALIVE_TEXT.format(me.first_name, "1.24"),
        file=ALIVE_PIC,
        parse_mode="htm",
        link_preview=False,
    )


@xbot.on(events.NewMessage(pattern="spoil", from_users=['me']))
async def _spoil_text(e):
    try:
        TEXT = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await e.reply("give text to spoil!")
    await e.respond("<span class='tg-spoiler'>{}</span>".format(TEXT), reply_to=e.reply_to_msg_id or e.id)
