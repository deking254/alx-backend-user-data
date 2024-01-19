#!/usr/bin/env python3
"""This is the Session Authentication module"""
from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """the session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is not None:
            if type(user_id) == str:
                session_id = str(uuid.uuid4())
                self.user_id_by_session_id[session_id] = user_id
                return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is not None:
            if type(session_id) == str:
                return self.user_id_by_session_id.get(session_id)
