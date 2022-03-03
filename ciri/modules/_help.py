from .. import bot

cmds = ["Alive", "Autodp", "Eval", "Spotdl"]
from telethon import events, functions, Button

from ..utils import ciri_cmd, eor


@bot.on(events.InlineQuery(pattern="help"))
async def help_menu(e):
    string = "Help menu for Ciri."
    buttons = []
    btn = []
    for x in cmds:
       if len(btn) == 2:
          buttons.append(btn)
          btn = []
       btn.append(Button.Inline(x, x.lower()))
    if len(btn) != 0:
      buttons.append(btn)
    result = await e.builder.article(string, buttons=buttons)
    await e.answer([result])

@ciri_cmd(pattern="help")
async def help_show(e):
 bot_get = await bot.get_me()
 r = await e.client.inline_query("@" + bot_get.username, "help")
 await r[0].click(
                e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True
            )
 await e.delete()

@ciri_cmd(pattern="dc")
async def _(e):
    if e.fwd_from:
        return
    result = await e.client(functions.help.GetNearestDcRequest())
    res = (
        "**Current DC:** {}\n**Nearest DC:** {}\n**Country:** {}".format(
            result.this_dc, result.nearest_dc, result.country
        )
    )
    await eor(e, res)
