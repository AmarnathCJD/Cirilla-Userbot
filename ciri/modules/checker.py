from ciri.utils import ciri_cmd, eor

@ciri_cmd(pattern="ck")
async def chk(e):
  await eor(e, 'rex gei')
