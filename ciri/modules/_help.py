from telethon import Button, events, functions

from .. import HelpStr, bot
from ..utils import ciri_cmd, eor

cmds = ["Alive", "Admin", "Dp", "Eval", "Spotdl", "Torr", "StickTools"]


main_help_menu = [
    [
        Button.inline("Plugins", data="uh_Official_"),
        Button.inline("Addons", data="uh_Addons_"),
    ],
    [
        Button.inline("Owner Tools", data="ownr"),
        Button.url("Settings", url=f"https://t.me/aiko_robot?start=set"),
    ],
    [Button.inline("Close", data="close")],
]


@bot.on(events.InlineQuery(pattern="help"))
async def help_menu(e):
    string = "Here is the help menu for Ciri."
    buttons = []
    btn = []
    for x in cmds:
        if len(btn) == 3:
            buttons.append(btn)
            btn = []
        btn.append(Button.inline(x, "help_" + x.lower()))
    if len(btn) != 0:
        buttons.append(btn)
    buttons.append([Button.inline("Back", "help_back")])
    result = e.builder.article(title=string, text=string, buttons=buttons)
    await e.answer([result])


@bot.on(events.InlineQuery(pattern="help_mm"))
async def help_men(e):
    string = """
Bᴏᴛ Oғ 4☈ RᴇxMᴏᴅZ🇷🇺『𝙸𝚅𝙰𝚁』

Mᴀɪɴ Mᴇɴᴜ

Pʟᴜɢɪɴs ~ 77
Aᴅᴅᴏɴs ~ 85
Tᴏᴛᴀʟ Cᴏᴍᴍᴀɴᴅs ~ 562
"""
    r = await e.builder.photo(
        file="https://i.ibb.co/vJbkYjz/20190524-172719.jpg",
        text=string,
        buttons=main_help_menu,
    )
    await e.answer([r])


@ciri_cmd(pattern="help")
async def help_menu(e):
    bot_get = await bot.get_me()
    r = await e.client.inline_query("@" + bot_get.username, "help_mm")
    await r[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
    await e.delete()


@bot.on(events.CallbackQuery(pattern="uh_Official_"))
async def help_show(e):
    bot_get = await bot.get_me()
    r = await e.client.inline_query("@" + bot_get.username, "help")
    await r[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
    await e.delete()


@bot.on(events.CallbackQuery(pattern="help(\_(.*))"))
async def help_show(e):
    p = e.pattern_match.group(1)
    if p in HelpStr:
        string = "Help for {}/n**Description:** ".format(p)
        string += HelpStr[p]["description"]
        string += "\n**Usage:** "
        string += HelpStr[p]["usage"]
        await e.edit(string, buttons=Button.inline("Back", "help_back"))
    else:
        await e.answer("No help found for this plugin.", alert=True)


@ciri_cmd(pattern="dc")
async def _(e):
    if e.fwd_from:
        return
    result = await e.client(functions.help.GetNearestDcRequest())
    res = "**Current DC:** {}\n**Nearest DC:** {}\n**Country:** {}".format(
        result.this_dc, result.nearest_dc, result.country
    )
    await eor(e, res)


@bot.on(events.CallbackQuery(pattern="help_(.*?)"))
async def cb_gelp(e):
    data = e.data.decode()
    await e.answer(data, alert=True)
