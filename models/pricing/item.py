from typing import Dict
import re
from bs4 import BeautifulSoup
import requests
import uuid
from dataclasses import dataclass, field
from common.database import Database
from models.model import Model


@dataclass(eq=False)
class Item(Model):

    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

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
            "query": self.query,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, _id) -> "Item":
        item = Database.find_one("items", {"_id": _id})
        return cls(**item)
