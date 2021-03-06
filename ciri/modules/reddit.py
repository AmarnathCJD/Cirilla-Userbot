import json
import os
import subprocess

import requests
from bs4 import BeautifulSoup

from ciri import HelpStr
from ciri.utils import ciri_cmd, eor


@ciri_cmd(pattern="red(?:dit)? (.*)")
async def reddit(e):
    url = e.pattern_match.group(1)
    if not url:
        return await e.edit("`No url provided?`")
    if not "reddit.com" in url:
        return await e.edit("`Invalid reddit url.`")
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    if not r.status_code == 200:
        return await e.edit("`Invalid reddit url, returned 404.`")
    post_id = get_post_id(url)
    vid, aud, title = get_download_url(post_id, r)
    msg = await eor(e, f"`Downloading...`")
    file = download_files(aud, vid, title)
    await msg.delete()
    await e.client.send_file(e.chat_id, file, caption=f"`{title}`")


def get_post_id(url: str) -> str:
    post_id = url[url.find("comments/") + 9 :]
    post_id = f"t3_{post_id[:post_id.find('/')]}"
    return post_id


def get_download_url(post_id: str, data: bytes):
    soup = BeautifulSoup(data.content, "html.parser")
    required_js = soup.find("script", id="data")
    json_data = json.loads(required_js.text.replace("window.___r = ", "")[:-1])
    title = json_data["posts"]["models"][post_id]["title"]
    title = title.replace(" ", "_")
    dash_url = json_data["posts"]["models"][post_id]["media"]["dashUrl"]
    height = json_data["posts"]["models"][post_id]["media"]["height"]
    if height == "1080":
        height = "480"
    dash_url = dash_url[: int(dash_url.find("DASH")) + 4]

    return f"{dash_url}_{height}.mp4", f"{dash_url}_audio.mp3", title


def download_files(a, v, title="reddit"):
    with requests.get(a) as r:
        if r.status_code == 200:
            with open(f"{title}_aud.mp3", "wb") as f:
                f.write(r.content)
        else:
            with requests.get(a.split("DASH_audio.mp3")[0] + "audio") as r:
                if r.status_code == 200:
                    with open(f"{title}_aud.mp3", "wb") as f:
                        f.write(r.content)
    with requests.get(v) as r:
        if r.status_code == 200:
            with open(f"{title}_vid.mp4", "wb") as f:
                f.write(r.content)
        else:
            with requests.get(v.split(".mp4")[0]) as r:
                if r.status_code == 200:
                    with open(f"{title}_vid.mp4", "wb") as f:
                        f.write(r.content)
    subprocess.call(
        [
            "ffmpeg",
            "-i",
            f"{title}_vid.mp4",
            "-i",
            f"{title}_aud.mp3",
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "copy",
            f"{title}.mp4",
        ]
    )
    os.remove(f"{title}_vid.mp4")
    os.remove(f"{title}_aud.mp3")
    return f"{title}.mp4"


HelpStr.update(
    {
        "reddit": {
            "red(ddit)": {
                "Description": "Downloads the audio and video from a reddit post.",
                "Usage": "red(ddit <url>)",
            },
        }
    }
)
