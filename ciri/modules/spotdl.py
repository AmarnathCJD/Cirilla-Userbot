import asyncio

from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="spotdl", allow_sudo=True)
async def spot_dl(e):
    try:
        query = e.text.split(maxsplit=1)[1]
    except IndexError:
        return await eor(e, "Song query was not provided.")
    cmd = "spotdl '{}'".format(query)
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    try:
        file_name = os.listdir("spotdl-temp")
    except:
        return await eor(e, "Failed to download song, spotify API refused to connect.")
    print(file_name)
