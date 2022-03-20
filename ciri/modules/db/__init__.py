from os import getenv

DB_URL = getenv("MONGO_DB_URL")

from pymongo import MongoClient
from telethon import types
DB = MongoClient(DB_URL)["ciri"]


def set_dp(id, access_hash, file_reference, type):
    DB.main.update_one(
        {"uid": "dp"},
        {
            "$set": {
                "id": id,
                "acess_hash": access_hash,
                "file_reference": file_reference,
                "type": type,
            }
        },
        upsert=True,
    )


def get_dp():
    x=DB.main.find_one({"uid": "dp"})
    if x:
        return x
    else:
        return types.Document(id=5888843716973562956, access_hash=8845595446721316165, file_reference=b'\x04H\xdeIR\x00\x06I\xc8b6\xfd\xfe\xb1~\xcd\xc9\xc8\xa7-\x8f\xa0\xbc`\x7f\xd6\xef\xee\x19')
