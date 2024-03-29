#!/usr/bin/env python3
'''
API authentication.
'''


from flask import request
from typing import List, TypeVar


class Auth():
    '''class to manage API authentication.'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth'''
        if path not in excluded_paths and path is None\
                and excluded_paths is None or not excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        '''authorization header'''
        if request is None or "Authorization" not in request:
            return None
        else:
            return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None
