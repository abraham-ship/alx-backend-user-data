#!/usr/bin/env python3
'''Hash password'''
import bcrypt
from user import User
from db import DB
from uuid import uuid4
from typing import Union


def _generate_uuid() -> str:
    '''Generate UUIDs
    Return:
        string representation of a new UUID '''
    return str(uuid4())


def _hash_password(password: str) -> str:
    '''Hash the input password with salt using bcrypt.hashpw
    Args:
    password (str): input passsword
    Return:
        bytes: The salted hash of the input password'''
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        '''Hash the input password with salt using bcrypt.hashpw
        Args:
            password (str): input passsword
        Return:
            bytes: The salted hash of the input password'''
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt=salt)
        return hash_password

    def register_user(self, email: str, password: str) -> User:
        '''register a new user
        Args:
            email (str): user email
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

    def valid_login(self, email: str, password: str) -> bool:
        '''try to locate a user by email and validate with password
        Agrs:
            email (str): user email
            password (str): user password
        Returns:
            True if match is found otherwise False'''
        user = self._db.find_user_by(email=email)
        return bcrypt.checkpw(password.encode('utf-8'),
                              user.hashed_password.encode('utf-8'))

    def create_session(self, email: str) -> str:
        '''find the user corresponding to the email,
        generate a new UUID and store it in the database
        as the user’s session_id
        Return:
            session ID'''
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        '''find user by session_id'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        '''updates the corresponding user’s session ID to None'''
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(found_user.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        '''find user and update user's reset token with UUID'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(found_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''find user and update user's hash_password and reset_token to None'''
        if reset_token is None or password is None:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
