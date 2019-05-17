from common.utils import Utils
from dataclasses import dataclass, field
from models.model import Model
import uuid


@dataclass(eq=False)
class Spending(Model):

    collection: str = field(init=False, default="spending")
    title: str
    category: str
    price: float
    user_email: str
    is_expense: bool
    date: str = field(default_factory=lambda: Utils.get_date())
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self):
        return {
            "_id": self._id,
            "user_email": self.user_email,
            "title": self.title,
            "category": self.category,
            "price": self.price,
            "date": self.date,
            "is_expense": self.is_expense
        }

