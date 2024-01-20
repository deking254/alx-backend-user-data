#!/usr/bin/env python3
"""the module to handle session authentication views"""
from api.v1.views import app_views
from flask import request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def parameter_handler():
    """retrieve email and password parameters"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return {"error": "email missing"}, 400
    if password is None or password == '':
        return {"error": "password missing"}, 400
    users = User.search({'email': email})
    if len(users) == 0:
        return {"error": "no user found for this email"}, 404
    for user in users:
        if user.is_valid_password(password) is False:
            return {"error": "wrong password"}, 401
    from api.v1.app import auth
    user = User()
    user.email = email
    user.password = password
    user.save()
    session_id = auth.create_session(user.id)
    response = make_response(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
