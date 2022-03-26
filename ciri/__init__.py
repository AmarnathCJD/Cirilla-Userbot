import io
import logging
import os
import time

import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession

# setup logger
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
)
load_dotenv()

# __Cirilla-Userbot__# [© 2021- 2022]
T = []
# shr


class Owner:
    ID = 0
    FirstName = ""
    LastName = ""
    Username = ""
    Mention = ""
    Bot = ""
    Messages = []

    def __init__(
        self, id=0, first_name="", last_name="", username="", bot="", messages=[]
    ):
        self.ID = id
        self.FirstName = first_name
        self.LastName = last_name
        self.Username = username
        self.Mention = "<a href='tg://user?id={}'>{}</a>".format(
            self.ID, self.FirstName
        )
        self.Bot = bot
        self.Messages = messages

    def __str__(self):
        return f"{self.ID} {self.FirstName} {self.LastName} ({self.Username})"

    def set_user(self, id, first_name="", last_name="", username="", bot=""):
        self.ID = id
        self.FirstName = first_name
        self.LastName = last_name
        self.Username = username
        self.Mention = "<a href='tg://user?id={}'>{}</a>".format(
            self.ID, self.FirstName
        )
        self.Bot = bot

    def add_msg(self, msg):
        self.Messages.append(msg)

    def get_msgs(self):
        return self.Messages


Master = Owner()
HelpStr = {}
StartTime = time.time()

# ENV
API_KEY = int(os.getenv("API_KEY"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
STRING_SESSION = os.getenv("STRING_SESSION")
CMD_HANDLERS = os.getenv("CMD_HANDLER")
ALIVE_PIC = os.getenv("ALIVE_PHOTO")
LOG_CHAT = int(os.getenv("LOG_CHAT"))
THUMB = os.environ.get("THUMB", "https://te.legra.ph/file/0f54f2801ef1baea71f95.jpg")

if not CMD_HANDLERS:
    CMD_HANDLERS = "."

BytesFile = requests.get(THUMB)
THUMB_FILE = io.BytesIO(BytesFile.content)

# userbot client
userbot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)

# bot client
bot = TelegramClient(None, API_KEY, API_HASH)

# database
if MONGO_DB_URI:
    db = MongoClient(MONGO_DB_URI)
else:
    db = None

FULL_SUDO = []
SUDO_USERS = []
