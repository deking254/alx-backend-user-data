#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()
auth.register_user(email, password)
auth.get_reset_password_token(email)
session = auth.create_session(email)
auth.get_reset_password_token
user = auth.get_user_from_session_id(session)
auth.destroy_session(user.id)
usr = auth._db.find_user_by(id=user.id)
