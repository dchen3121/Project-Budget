from typing import Dict
import pymongo


class Database:
    URI = "mongodb://127.0.0.1:27017/pricing"
    DATABASE = pymongo.MongoClient(URI)

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)
