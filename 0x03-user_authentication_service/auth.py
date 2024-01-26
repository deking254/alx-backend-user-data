#!/usr/bin/env python3
"""this module deals with encrypting person info"""
import bcrypt
from user import User
from sqlalchemy import select
from db import DB
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str = None) -> bytes:
    """returns the hashed password"""
    if password is not None:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))


def _generate_uuid() -> str:
    """generates and returns uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creates a new user"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_pass = _hash_password(password)
            self._db.add_user(email, hashed_pass)

    def valid_login(self, email: str, password: str) -> bool:
        """validates the user credentials"""
        try:
            user = self._db.find_user_by(email=email)
            a = bcrypt.checkpw(password.encode(),
                               dict(user).get('hashed_password'))
            return a
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ takes an email string argument and returns
        the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str):
        """takes a single session_id string argument and
        returns the corresponding User or None"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: int):
        """set the session_id of a user to None"""
        try:
            user = self._db.find_user_by(id=user_id)
            if user is not None:
                self._db.update_user(user_id, session_id=None)
                return None
        except Exception:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """generates a token and assigns to the reset_token field"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            if user is not None:
                self._db.update_user(user.id, reset_token=reset_token)
                return reset_token
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """updating the user password"""
        user = self._db.find_user_by(reset_token=reset_token)
        if user is not None:
            self._db.update_user(user.id, reset_token=None,
                                 hashed_password=_hash_password(password))
        return None
