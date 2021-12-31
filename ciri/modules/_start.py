from ciri.utils import ciri_cmd


@ciri_cmd(pattern="start")
async def _start(e):
    await e.edit("smd 7; ub handler sucess")
