#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
if getenv('AUTH_TYPE') is not None:
    if getenv('AUTH_TYPE') == 'basic_auth':
        auth = BasicAuth()
    else:
        auth = Auth()

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """unauthorized error"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def no_access(error) -> str:
    """error handler for authenticated but no access to resource"""
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def handle_request():
    """handles the request before rendering"""
    if auth is not None:
        list_of_auth_endpoints = [
                '/api/v1/status/',
                '/api/v1/unauthorized/',
                '/api/v1/forbidden/']
        if auth.require_auth(request.path, list_of_auth_endpoints):
            if auth.authorization_header(request) is None:
                abort(401)
            else:
                if auth.current_user(request) is None:
                    abort(403)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
