#!/usr/bin/env python3
"""this is the template file for the authenticatins system"""
from flask import request
from typing import List, TypeVar


class Auth():
    """this is the class for authenticating"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false or true depending on if authenticatin is required"""
        if excluded_paths is not None:
            if len(excluded_paths) == 0:
                return True
        else:
            return True
        if path is None or path not in excluded_paths:
            if path is not None:
                if path[-1] == '/':
                    if path[0:-1] in excluded_paths:
                        return False
                else:
                    path = path + '/'
                    if path in excluded_paths:
                        return False
            return True
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """returns the authorization header"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the user accessing the server"""
        return None
