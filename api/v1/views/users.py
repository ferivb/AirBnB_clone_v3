#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'User' """


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, user
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getAllUsers():
    """Retrieves the list of all User objects"""
    users = []
    for user in storage.all("User").values():
        # Using to_dict to retrieve an object into a valid JSON
        users.append(user.to_dict())

    return jsonify(users)
