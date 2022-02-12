from os import getenv

DB_URL = getenv("MONGO_DB_URI")

from pymongo import MongoClient

DB = MongoClient(DB_URL)["ciri"]

def set_dp(id, access_hash, file_reference, type):
    DB.main.update_one(
        {"id": "dp"},
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
    return DB.main.find_one({"id": "dp"})
