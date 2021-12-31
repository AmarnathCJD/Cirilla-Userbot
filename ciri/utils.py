from telethon import functions, events, types, errors
from ciri import LOG_CHAT, SUDO, FULL_SUDO, OWNER_ID, CMD_HANDLERS, ub

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
        ub.add_event_handler(func, events.NewMessage(**args))
        return func
 return decorator

    
