import sys

from ciri import BOT_TOKEN, bot, userbot
from ciri.utils import load_modules, startup_tasks

try:
    userbot.start()
    bot.start(bot_token=BOT_TOKEN)
except Exception:
    sys.exit(1)

userbot.loop.run_until_complete(startup_tasks())
load_modules()
print("cirilla Userbot Is Alive")
userbot.run_until_disconnected()
