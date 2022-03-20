from os import getenv

DB_URL = getenv("MONGO_DB_URL")

from pymongo import MongoClient

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
        return {"id": "https://te.legra.ph/file/cb37180e3aaa92dac6f40.jpg", "type": "link"}
