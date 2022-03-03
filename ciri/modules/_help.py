from .. import bot
cmds = ["Alive", "Autodp", "Eval", 'Spotdl']
from ..utils import ciri_cmd, eor
from telethon import events

@bot.on(events.InlineQuery(pattern="help"))
async def help_menu(e):
 await eor(e, "Hi")


@ciri_cmd.on(pattern="dc")
async def _(e):
    if e.fwd_from:
        return
    result = await e.client(functions.help.GetNearestDcRequest())
    await eor(e, result.stringify())
