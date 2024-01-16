#!/usr/bin/env python3
'''
API authentication.
'''


from flask import request
from typing import List


class Auth():
    '''class to manage API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth'''
        return False

    def authorization_header(self, request=None) -> str:
        '''authorization header'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None