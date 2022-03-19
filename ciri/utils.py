import glob
import importlib
import logging
import sys
from pathlib import Path
import os
from telethon import events

from ciri import CMD_HANDLERS, FULL_SUDO, OWNER_ID, SUDO, bot, userbot


def ciri_cmd(**args):
    args["pattern"] = "^[" + CMD_HANDLERS + "](?i)" + args["pattern"]
    if args.get("allow_sudo"):
        FROM_USERS = SUDO
        FROM_USERS.append(OWNER_ID)
        args["from_users"] = FROM_USERS
        del args["allow_sudo"]
    elif args.get("full_sudo"):
        FROM_USERS = FULL_SUDO
        FROM_USERS.append(OWNER_ID)
        args["from_users"] = FROM_USERS
        del args["full_sudo"]
    else:
        args["from_users"] = OWNER_ID

    def decorator(func):
        async def wrapper(ev):
            try:
                await func(ev)
            except BaseException as exception:
                logging.info(exception)

        userbot.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator


async def eor(e, msg, file=None, parse_mode="md", link_preview=False):
    if e.sender_id == OWNER_ID:
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
    OWNER_ID = (await userbot.get_me()).id
    os.environ["OWNER_ID"] = OWNER_ID
