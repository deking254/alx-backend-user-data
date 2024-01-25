#!/usr/bin/env python3
"""this module implements the flask framework"""
from auth import Auth
from flask import Flask, jsonify, request, make_response, abort

AUTH = Auth()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """handles the route '/'"""
    return jsonify({"message": "Bienvenue"})

@app.route('/users', methods=['POST'])
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        payload = {"email": "<registered email>", "message": "user created"}
        payload['email'] = email
        return  jsonify(payload)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route('/sessions', methods=['POST'])
def login():
    """determines the eligibility of a user to login"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = make_response({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
    return abort(401)

@app.route('/sessions', methods=['DELETE'])
def logout():
    """executes the destroy session"""
    session_id = request.cookies.get('session_id')
    if session_id is not None:
        AUTH.destroy_session(session_id)
        return index()
    else:
        return abort(403)

@app.route('/profile', methods=['GET'])
def profile():
    """returns the user from the current session id"""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user is not None:
        user_email = user.email
        return jsonify({"email": user_email})
    else:
        return abort(403)

@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        payload = {"email": email, "reset_token": reset_token}
        return jsonify(payload), 200
    except ValueError:
        return abort(403)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
