import sys

from ciri import userbot, bot, BOT_TOKEN
from ciri.utils import get_owner, load_modules

try:
    userbot.start()
    bot.start(bot_token=BOT_TOKEN)
except Exception as exc:
    sys.exit(1)

load_modules()
print("Cirilla Userbot Is Alive")

userbot.loop.run_until_complete(get_owner())
userbot.run_until_disconnected()
