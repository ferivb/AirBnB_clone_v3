#!/usr/bin/python3
"""
States view for API
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, state


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Gets the state information for all states"""
    states = []
    for states in storage.all("State").values():
        states.append(states.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Gets the state information, for a specified state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a state using it's id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        storage.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state and saves it in storage"""
    state = request.get_json()
    if state is None:
        abort(400, "Not a JSON")
    elif "name" not in state.keys():
        abort(400, "Missing name")
    else:
        new_state = state.State(**state)
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """Updates a state and save changes in storage"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    state = request.get_json()
    if state is None:
        abort(400, "Not a JSON")
    else:
        for key, value in state.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(obj, key, value)
        storage.save()
        result = obj.to_dict()
        return jsonify(result), 200
