import sys
import time

from ciri import BOT_TOKEN, OWNER_ID, bot, userbot
from ciri.utils import get_owner, load_modules

try:
    userbot.start()
    bot.start(bot_token=BOT_TOKEN)
except Exception:
    sys.exit(1)
userbot.loop.run_until_complete(get_owner())
time.sleep(3)
print(OWNER_ID)
load_modules()
print("Cirilla Userbot Is Alive")
userbot.run_until_disconnected()
