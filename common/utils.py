import re
import datetime
from passlib.hash import pbkdf2_sha512
# pbkdf2 is an algorithm for encryption


class Utils:

    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        if email_address_matcher.match(email):
            return True
        return False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password: str, hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password, hashed_password)

    @staticmethod
    def get_date():
        """
        Gets the current date and outputs in YYYY-MM-DD form
        :return: the current date
        """
        now = datetime.datetime.now()
        return f"{now.year}-{now.month:02d}-{now.day:02d}"

    @staticmethod
    def get_date_accurate():
        now = datetime.datetime.now()
        return f"{now.year}-{now.month:02d}-{now.day:02d},{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
