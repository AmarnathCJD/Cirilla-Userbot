import glob
import importlib
import logging
import sys
from pathlib import Path

from telethon import events

from ciri import CMD_HANDLERS, LOG_CHAT, Master, bot, userbot

errors = {"latest": "null"}


def ciri_cmd(**args):
    args["pattern"] = "^[" + CMD_HANDLERS + "](?i)" + args["pattern"]
    if args.get("allow_sudo"):
        del args["allow_sudo"]
    elif args.get("full_sudo"):
        del args["full_sudo"]
    args["outgoing"] = True

    def decorator(func):
        async def wrapper(ev):
            try:
                await func(ev)
            except BaseException as exception:
                logging.info(exception)
                errors["latest"] = exception

        userbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


async def eor(e, msg, file=None, parse_mode="md", link_preview=False):
    if e.sender_id == Master.ID:
        return await e.edit(
            msg, file=file, parse_mode=parse_mode, link_preview=link_preview
        )
    else:
        return await e.reply(
            msg, file=file, parse_mode=parse_mode, link_preview=link_preview
        )


def load_modules():
    for x in glob.glob("ciri/modules/*.py"):
        with open(x) as f:
            name = Path(f.name).stem.replace(".py", "")
            spec = importlib.util.spec_from_file_location(
                "ciri.modules.{}".format(name), Path("ciri/modules/{}.py".format(name))
            )
            mod = importlib.util.module_from_spec(spec)
            mod.bot = userbot
            mod.tbot = bot
            mod.eor = eor
            spec.loader.exec_module(mod)
            sys.modules["ciri.modules." + name] = mod
            print("Import " + name.upper() + " module")


async def get_owner():
    user = await userbot.get_me()
    botme = await bot.get_me()
    Master.set_user(
        user.id,
        user.first_name or "",
        user.last_name or "",
        user.username or "",
        bot=botme.username,
    )


async def send_start_message():
    if LOG_CHAT != -100 and LOG_CHAT != 0:
        msg = """**CIRI has been deployed!
➖➖➖➖➖➖➖➖➖➖
UserMode: {}
Assistant: {}
➖➖➖➖➖➖➖➖➖➖
Support: @RoseLoverX_Support
➖➖➖➖➖➖➖➖➖➖**""".format(
            Master.FirstName + " " + Master.Mention, Master.Bot
        )
        await userbot.send_message(LOG_CHAT, msg)


async def startup_tasks():
    await get_owner()
    await send_start_message()
