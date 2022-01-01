from ciri.utils import ciri_cmd, eor

@ciri_cmd(pattern="del", allow_sudo=True)
async def _del(e):
  if not e.reply_to:
    return await eor(e, "Reply to msg to delete it!")
  try:
    reply = await e.get_reply_message()
    await reply.delet()
  except Exception as exc:
    await eor(e, "failed to delete, " + str(exc))
