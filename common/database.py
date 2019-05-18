from typing import Dict
import pymongo
import os


class Database:
    # For localhost testing
    # URI = "mongodb://127.0.0.1:27017/pricing"

    URI = os.environ.get('MONGOLAB_URI')
    DATABASE = pymongo.MongoClient(URI).get_database()

    @staticmethod
    def insert(collection: str, data: Dict):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:  # cursor kind of behaves like a list
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict):
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict):
        Database.DATABASE[collection].remove(query)

    @staticmethod
    def find_all_sorted_by(collection: str, query: Dict, key: str, ascending: bool):
        if ascending:
            return Database.DATABASE[collection].find(query).sort(key, pymongo.ASCENDING)
        return Database.DATABASE[collection].find(query).sort(key, pymongo.DESCENDING)
