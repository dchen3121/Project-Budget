from typing import Dict
import re
from flask import Flask
from bs4 import BeautifulSoup
import requests
import uuid
from common.database import Database


class Item:
    def __init__(self, url: str, tag_name: str, query: Dict, _id: str = None):
        """
        Initializes an item object
        :param url: the url of the thing we are looking to buy
        :param tag_name: the tag we are looking for (e.g. a 'p' tag)
        :param query: the query we are searching for for the item, in dictionary format
        :param _id: the id of the item, may be randomly generated with uuid
        """
        self.url = url
        self.tag_name = tag_name
        self.query = query
        self.price = None
        self.collection = "pricing"
        self._id = _id or uuid.uuid4().hex

    def __repr__(self):
        return f"<item {self.url}>"

    def load_price(self) -> float:
        """
        Given an item, returns its price in float in $
        :return: float representing the price of the object in dollars
        """
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile(r"(\d+,?\d*\.\d\d)")
        match = pattern.search(string_price)
        found_price = match.group(1)
        without_commas = found_price.replace(",", "")
        self.price = float(without_commas)
        return self.price

    def json(self) -> Dict:
        """
        Returns a json type representation of the item object
        :return: a dictionary type containing all the information of the Item
        """
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query
        }

    def save_to_mongo(self):
        """
        Saves the object to mongoDB
        :return: void
        """
        Database.insert(self.collection, self.json())
