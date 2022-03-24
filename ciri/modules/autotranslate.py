from google_translate_py import AsyncTranslator

from ciri import HelpStr
from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="at(?: |$)(.*)")
async def _at(e):
    payload = e.text.split(maxsplit=2)
    if len(payload) == 2:
        text = payload[2]
        lang = payload[1]
    else:
        text = payload[1]
        lang = "en"
    tr = await AsyncTranslator().translate(text, "", lang)
    await eor(e, tr)  # eor(e, tr)


HelpStr["autotranslate"]={
        "at": {
            "description": "Auto Translate text while typing",
            "usage": ".at <lang> <text>",
        }
    }

