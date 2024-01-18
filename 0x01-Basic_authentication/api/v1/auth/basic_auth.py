#!/usr/bin/env python3
"""this is the basic authentication file"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """handles basic authentication"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """extracts the second part of a basic header"""
        if authorization_header is not None:
            if type(authorization_header) == str:
                if authorization_header.startswith('Basic '):
                    item_after_space = authorization_header.split(' ')[1]
                    return item_after_space
        return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """returns the decoded values of a base64 string"""
        if base64_authorization_header is not None:
            if type(base64_authorization_header) == str:
                try:
                    a = base64.b64decode(base64_authorization_header)
                    return a.decode('utf-8')
                except Exception:
                    pass
        return None
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """returns email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is not None:
            if type(decoded_base64_authorization_header) == str:
                if decoded_base64_authorization_header.find(':') >= 0:
                    email_and_pass = decoded_base64_authorization_header.split(':')
                    return (email_and_pass[0], email_and_pass[1])
        return (None, None)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns an instance of user with the email specified"""
        if user_email is not None:
            if type(user_email) == str:
                return User.search({user_email})[0]
        return None
