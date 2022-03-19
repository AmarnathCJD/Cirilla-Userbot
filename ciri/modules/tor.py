import math
import os
import math
import aria2p
from ciri.utils import ciri_cmd, eor
from asyncio import sleep
from pathlib import Path
from subprocess import PIPE, Popen
from requests import get

def subprocess_run(cmd):
    subproc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True, universal_newlines=True)
    talk = subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        return
    return talk


def aria_start():
    trackers_list = get(
        "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt"
    ).text.replace("\n\n", ",")
    trackers = f"[{trackers_list}]"
    cmd = f"aria2c \
          --enable-rpc \
          --rpc-listen-all=false \
          --rpc-listen-port=6800 \
          --max-connection-per-server=10 \
          --rpc-max-request-size=1024M \
          --check-certificate=false \
          --follow-torrent=mem \
          --seed-time=600 \
          --max-upload-limit=0 \
          --max-concurrent-downloads=1 \
          --min-split-size=10M \
          --follow-torrent=mem \
          --split=10 \
          --bt-tracker={trackers} \
          --daemon=true \
          --allow-overwrite=true"
    process = subprocess_run(cmd)
    aria2 = aria2p.API(
        aria2p.Client(host="http://localhost", port=6800, secret="")
    )
    return aria2


aria2p_client = aria_start()

async def check_metadata(gid):
    t_file = aria2p_client.get_download(gid)
    if not t_file.followed_by_ids:
        return None
    new_gid = t_file.followed_by_ids[0]
    return new_gid

async def check_progress_for_dl(gid, message, previous):
    complete = False
    while not complete:
        try:
            t_file = aria2p_client.get_download(gid)
        except:
            return await message.edit("Download cancelled by user ...")
        complete = t_file.is_complete
        is_file = t_file.seeder
        try:
            if t_file.error_message:
                print(str(t_file.error_message))
                await message.edit(str(t_file.error_message))
            if not complete and not t_file.error_message:
                percentage = int(t_file.progress)
                downloaded = percentage * int(t_file.total_length) / 100
                prog_str = f"** Downloading! @ {t_file.progress_string()}**"
                if is_file is None :
                   info_msg = f"**Connections:**  `{t_file.connections}`\n"
                else :
                   info_msg = f"**Connection:**  `{t_file.connections}` \n" \
                       f"**Seeds:**  `{t_file.num_seeders}` \n"
                msg = (
                    f"`{prog_str}` \n\n"
                    f"**Name:**  `{t_file.name}` \n"
                    f"**Completed:**  `{humanbytes(downloaded)}` \n"
                    f"**Total:**  `{t_file.total_length_string()}` \n"
                    f"**Speed:**  `{t_file.download_speed_string()}` \n"
                    f"{info_msg}"
                    f"**ETA:**  `{t_file.eta_string()}` \n"
                    f"**GID:**  `{gid}`"
                )
                if msg != previous:
                    await message.edit(msg)
                    previous = msg
            else:
                if complete and not t_file.name.lower().startswith("[metadata]"):
                    return await message.edit(
                        f"**Successfully Downloaded {t_file.name}** \n\n"
                        f"> Size:  `{t_file.total_length_string()}` \n"
                        f"> Path:  `{t_file.name}`"
                    )
                await message.edit(msg)
            await sleep(8)
            await check_progress_for_dl(gid, message, previous)
        except Exception as e:
            if "not found" in str(e) or "'file'" in str(e):
                if "Your Torrent/Link is Dead." not in message.text:
                    await message.edit(f"**Download Canceled,** \n`{t_file.name}`")
            elif "depth exceeded" in str(e):
                t_file.remove(force=True)
                await message.edit(
                    f"**Download Auto Canceled :**\n`{t_file.name}`\nYour Torrent/Link is Dead."
                )

@ciri_cmd(pattern="ariadl ?(.*)")
async def t_url_download(message):
    is_url, is_mag = False, False
    reply = await message.get_reply_message()
    args = message.pattern_match.group(1)
    message = await eor(message, "...")
    if reply and reply.document and reply.file.ext == ".torrent":
        tor = await message.client.download_media(reply)
        try:
            download = aria2p_client.add_torrent(
                tor, uris=None, options=None, position=None
            )
        except Exception as e:
            return await message.edit(f"**ERROR:**  `{e}`")
    elif args:
        if args.lower().startswith("http"):
            try:  # URL
                is_url = True
                download = aria2p_client.add_uris([args], options=None)
            except Exception as e:
                return await message.edit(f"**ERROR while adding URI** \n`{e}`")
        elif args.lower().startswith("magnet:"):
            is_mag = True
            try:  # Magnet
                download = aria2p_client.add_magnet(args, options=None)
            except Exception as e:
                return await message.edit(f"**ERROR while adding URI** \n`{e}`")
    else:
        return await message.edit("`No torrent given`")
    gid = download.gid
    await message.edit("`Processing......`")
    await check_progress_for_dl(gid=gid, message=message, previous="")
    if is_url:
        file = aria2p_client.get_download(gid)
        if file.followed_by_ids:
            new_gid = await check_metadata(gid)
            await check_progress_for_dl(gid=new_gid, message=message, previous="")
    elif is_mag:
        await sleep(6)
        new_gid = await check_metadata(gid)
        await check_progress_for_dl(gid=new_gid, message=message, previous="")

def humanbytes(size, decimal_places=2):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"