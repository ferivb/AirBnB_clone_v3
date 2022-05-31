#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'State' """


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getAllStates():
    """Retrieves the list of all State objects"""
    states = []
    for state in storage.all("State").values():
        # Using to_dict to retrieve an object into a valid JSON
        states.append(state.to_dict())

    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def getSingleState(state_id=None):
    """Retrieves a State object"""
    singleState = storage.get("State", state_id)
    if singleState is None:
        abort(404)
    else:
        return jsonify(singleState.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteState(state_id=None):
    """Deletes a State object"""
    singleState = storage.get("State", state_id)
    if singleState is None:
        abort(404)
    else:
        storage.delete(singleState)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def postState():
    """Create a state"""
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    elif "name" not in dict.keys():
        abort(400, "Missing name")
    else:
        new_state = state.State(**dict)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def putState(state_id=None):
    """Updates a State object"""
    # Retireve the state from storage using state_id
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    else:
        for key, val in dict.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(state, key, val)
        storage.save()
        updatedState = state.to_dict()
        return jsonify(updatedState), 200
