#!/usr/bin/env python3
'''Basic auth'''


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
