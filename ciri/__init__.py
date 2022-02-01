import logging
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession

load_dotenv()

# setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
)

# __Cirilla-Userbot__# [© 2021- 2022]

# ENV
API_KEY = int(os.getenv("API_KEY"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
STRING_SESSION = os.getenv("STRING_SESSION")
PORT = os.getenv("PORT")
SPTFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPTFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
CMD_HANDLERS = os.getenv("CMD_HANDLER")
REM_BG_API_KEY = os.getenv("REM_BG_API_KEY")
ALIVE_PIC = os.getenv("ALIVE_PHOTO")
OWNER_ID = int(os.getenv("OWNER_ID"))
LOG_CHAT = int(os.getenv("LOG_CHAT"))


if not CMD_HANDLERS:
    CMD_HANDLERS = "."


# userbot client
ub = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)

# bot client
bot = TelegramClient(None, API_KEY, API_HASH)

# database
if MONGO_DB_URL:
    db = MongoClient(MONGO_DB_URL)
else:
    db = None
    print("Database URL not found!")

FULL_SUDO = SUDO = []
