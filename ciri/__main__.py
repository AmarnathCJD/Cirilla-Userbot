import sys

from ciri import BOT_TOKEN, bot, ub
from ciri.utils import load_modules

try:
    bot.start(bot_token=BOT_TOKEN)
    ub.start()
except Exception as exc:
    print(exc)
    sys.exit(1)

load_modules()
Print("Ciri Userbot Is Alive")

ub.run_until_disconnected()
