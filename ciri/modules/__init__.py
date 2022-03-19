import telethon

from ciri.utils import eor


async def get_user(e):
    args = e.text.split(maxsplit=1)
    if e.reply_to_msg_id:
        user = await e.get_reply_message()
        user = user.sender_id
        if len(args) > 1:
            return user, args[1]
        else:
            return user, ""
    elif len(args) > 2:
        user = args[1]
        if args[2].isdigit():
            user = int(args[1])
        try:
            user = await e.client.get_entity(user)
        except BaseException as err:
            await eor(e, "`{}`".format(err))
            return None, ""
        if len(args) > 2:
            return user, args[2]
        else:
            return user, ""
    else:
        await eor(e, "`Reply to a user or specify one!`")
        return None, ""


async def get_user_from_id(user, e):
    if isinstance(user, str) and user.isdigit():
        user = int(user)
    try:
        user = await e.client.get_entity(user)
    except BaseException as err:
        await eor(e, "`{}`".format(err))
        return None, ""
    return user


async def CheckRights(e, right: str):
    if not e.chat.admin_rights:
        await eor(e, "You are not admin!")
        return False
    elif e.chat.admin_rights.get(right):
        return True
    else:
        await eor(e, "You don't have the right to use this command!")
        return False
    e.chat.admin_rights
