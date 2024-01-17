#!/usr/bin/env python3
"""this is the template file for the authenticatins system"""
import request from flask


class Auth():
    """this is the class for authenticating"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """returns false or true depending on if authenticatin is required"""
        return False

    def authorization_header(self, request=None) -> str:
        """returns the authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the user accessing the server"""
        return None
