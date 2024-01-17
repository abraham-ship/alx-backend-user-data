#!/usr/bin/env python3
'''Basic auth'''


from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    '''BasicAuth'''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''returns the Base64 part of the Authorization header
        for a Basic Authentication'''
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''returns the decoded value of a Base64
        string base64_authorization_header'''
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None
        try:
            decoded_value = base64.b64decode(
                    base64_authorization_header).decode('utf-8')
            return decoded_value
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''Basic - User credentials'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return (email, pwd)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''returns the User instance based on his email and password'''
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Get the authorization header from the request'''
        authorization_header = self.authorization_header(request)

        base64_authorization_header =
        self.extract_base64_authorization_header(authorization_header)

        decoded_value = self.decode_base64_authorization_header(
                base64_authorization_header)

        user_email, user_pwd = self.extract_user_credentials(decoded_value)
        user_instance = self.user_object_from_credentials(user_email, user_pwd)

        return user_instance
