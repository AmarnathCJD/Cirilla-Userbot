from os import getenv

from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession

# __Cirilla-Userbot__# [© 2021- 2022]

API_KEY = os.getenv("API_KEY")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
STRING_SESSION = os.getenv("STRING_SESSION")
PORT = os.getenv("PORT")
SPTFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPTFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# userbot client
ub = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)

# bot client
bot = TelegramClient(None, API_KEY, API_HASH)

# database
if MONGO_DB_URL:
    db = MongoClient(MONGO_DB_URL)
else:
    db = MongoClient("localhost", 27017)
    print("Database URL not found!, using sqlite.")
