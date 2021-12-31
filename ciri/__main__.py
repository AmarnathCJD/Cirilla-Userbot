from ciri.utils import load_modules
from ciri import ub, bot
import sys

try:
  bot.start(bot_token=BOT_TOKEN)
  ub.start()
except Exception as exc:
  print(exc)
  sys.exit(1)

load_modules()
Print("Ciri Userbot Is Alive")

ub.run_until_disconnected()
