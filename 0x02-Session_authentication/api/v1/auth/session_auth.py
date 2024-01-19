#!/usr/bin/env python3
'''new automation mechanism'''
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    '''empty class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''retrieves a Session ID for a user_id'''
        if session_id is None or not isinstance(session_id, str):
            return None
        return user_id_by_session_id.get('session_id')

    def current_user(self, request=None):
        ''' returns a User instance based on a cookie value'''
        session_id = self.session_cookie('_my_session_id')
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)
