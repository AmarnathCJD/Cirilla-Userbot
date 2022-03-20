import telethon

from ciri import HelpStr
from ciri.modules import CheckRights, get_user
from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="del", allow_sudo=True)
async def _del(e):
    if not e.reply_to:
        return await eor(e, "Reply to msg to delete it!")
    try:
        reply = await e.get_reply_message()
        await reply.delete()
    except Exception as exc:
        await eor(e, "failed to delete, " + str(exc))
    finally:
        await e.delete()


@ciri_cmd(pattern="ban", allow_sudo=True)
async def _ban(e: telethon.types.UpdateNewMessage):
    if not CheckRights(e, "ban_users"):
        return
    user, r = await get_user(e)
    if not user:
        return
    try:
        await e.client(
            telethon.functions.channels.EditBannedRequest(
                channel=e.chat_id,
                user_id=user.id,
                banned_rights=telethon.types.ChatBannedRights(view_messages=True),
            )
        )
    except Exception as err:
        await eor(e, "`{}`".format(err))
        return
    await eor(e, "`Banned`")


HelpStr.append(
    {
        "del": {"description": "Deletes a message.", "usage": "del"},
        "ban": {"description": "Bans a user.", "usage": "ban"},
    }
)
