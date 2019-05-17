from typing import List, TypeVar, Type, Dict, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):

    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    def save_to_mongo(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_mongo(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def json(self) -> Dict:
        raise NotImplementedError

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        things_from_db = Database.find(cls.collection, {})
        return [cls(**thing) for thing in things_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: Union[str, Dict]) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def find_many_by(cls, attribute: str, value: str) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, {attribute: value})]

    @classmethod
    def find_many_by_dict(cls, query: Dict) -> List[T]:
        return [cls(**elem) for elem in Database.find(cls.collection, query)]

    @classmethod
    def find_sorted_ascending(cls, query: Dict, key: str):
        return [cls(**elem) for elem in Database.find_all_sorted_by(cls.collection, query, key, True)]

    @classmethod
    def find_sorted_descending(cls, query: Dict, key: str):
        return [cls(**elem) for elem in Database.find_all_sorted_by(cls.collection, query, key, False)]
