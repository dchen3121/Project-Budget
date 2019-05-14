import re
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
