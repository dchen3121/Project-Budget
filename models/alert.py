from typing import Dict
from models.item import Item
import uuid
from flask import session
from models.model import Model
from models.user.user import User
from dataclasses import dataclass, field
from libs.mailgun import Mailgun


@dataclass(eq=False)
class Alert(Model):

    collection: str = field(init=False, default="alerts")
    item_id: str
    price_limit: float
    item_name: str
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "item_name": self.item_name,
            "user_email": self.user_email
        }

    def load_item_price(self) ->float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item_name} has reached a price under CAD ${self.price_limit}.\n"
                  f"Latest price: CAD ${self.item.price}.")
            '''
            Mailgun.send_mail(
                [self.user_email],
                f'Your item {self.item_name} has reached your desired price!',
                f'Your alert {self.item_name} has reached a price under CAD ${self.price_limit}.\n' +
                f'Latest price: CAD ${self.item.price}\nCheck out your item here: {self.item.url}',
                f'<h3>Your alert {self.item_name} has reached a price under CAD ${self.price_limit}.</h3>' +
                f'<h4>Latest price: CAD ${self.item.price}</h4>' +
                f'<h4>Check out your item here: {self.item.url}</h4>'
            )
            '''
