#!/usr/bin/env python3
'''Hash password'''
import bcrypt
from user import User
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        '''Hash the input password with salt using bcrypt.hashpw
        Args:
            password (str): input passsword
        Return:
            bytes: The salted hash of the input password'''
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt=salt)
        return hash_password

    def register_user(email: str, password: str) -> User:
        '''register a new user
        Args:
            email (str): user wmail
            password (str): user password
        Returns:
            User: The registered User object
        Raises:
            ValueError: if user email already provided'''
        existing_user = self._db.find_user_by(email=email)
        if existing_user:
            raise ValueError(f"User {email} already exists.")

        hashed_password = self._hash_password(password)
        new_user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
        return new_user
