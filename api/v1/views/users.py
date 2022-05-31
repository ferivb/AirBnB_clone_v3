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


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def getSingleUser(user_id=None):
    """Retrieves a User object"""
    singleUser = storage.get("User", user_id)
    if singleUser is None:
        abort(404)
    else:
        return jsonify(singleUser.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteUser(user_id=None):
    """Deletes a User object"""
    singleUser = storage.get("User", user_id)
    if singleUser is None:
        abort(404)
    else:
        storage.delete(singleUser)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def postUser():
    """Create a user"""
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    elif "email" not in dict.keys():
        abort(400, "Missing email")
    elif "password" not in dict.keys():
        abort(400, "Missing password")
    else:
        new_user = user.User(**dict)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def putUser(user_id=None):
    """Updates a User object"""
    # Retireve the user from storage using user_id
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    else:
        for key, val in dict.items():
            if key in ['id', 'email', 'created_at', 'updated_at']:
                pass
            else:
                setattr(user, key, val)
        storage.save()
        updatedUser = user.to_dict()
        return jsonify(updatedUser), 200
