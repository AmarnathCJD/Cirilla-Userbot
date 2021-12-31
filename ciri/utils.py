import logging

from telethon import events

from ciri import CMD_HANDLERS, FULL_SUDO, OWNER_ID, SUDO, ub


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
            except Exception as exception:
                logging.info(exception)

        ub.add_event_handler(wrapper, events.NewMessage(**args))
        return wrapper

    return decorator
