from telethon import Button, events, functions

from .. import HelpStr, Master, bot, userbot
from ..utils import Own, ciri_cmd, eor

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


@bot.on(events.InlineQuery(pattern="hedd"))
async def help_menuu(e):
    string = """
<b>Bᴏᴛ Oғ {}</b>

Mᴀɪɴ Mᴇɴᴜ

<b>Pʟᴜɢɪɴs ~ {}</b>
Tᴏᴛᴀʟ Cᴏᴍᴍᴀɴᴅs ~ .
""".format(
        Master.Mention,
        len(cmds),
    )
    r = await e.builder.article(
        title="1.0.0",
        text=string,
        buttons=main_help_menu,
        parse_mode="html",
    )
    await e.answer([r])


@ciri_cmd(pattern="help")
async def help_menu(e):
    r = await userbot.inline_query("@" + Master.Bot, "hedd")
    await r[0].click(e.chat_id, reply_to=e.reply_to_msg_id, hide_via=True)
    await e.delete()


@Own
@bot.on(events.CallbackQuery(pattern="uh_Official_"))
async def help_show(e):
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
    await e.edit(
        string,
        buttons=buttons,
        parse_mode="md",
        link_preview=False,
    )


@bot.on(events.CallbackQuery(pattern="help_(.*?)"))
async def help_show(e):
    p = e.pattern_match.group(1).decode("utf-8")
    p = p.split("_")[1]
    if p.lower() in HelpStr:
        string = "Help for {}/n**Description:** ".format(p)
        for key, val in HelpStr[p.lower()].items():
            string += "{} - {}\n".format(key, val["description"])
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
