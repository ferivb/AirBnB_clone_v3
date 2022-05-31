#!/usr/bin/python3
"""
States view for API
"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage, State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Gets state information for all states"""
    res = []
    for i in storage.all("State").values():
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Gets state information for specified state"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        return jsonify(s.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a state based on its id"""
    s = storage.get("State", state_id)
    if s is None:
        abort(404)
    else:
        storage.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new state"""
    if not request.get_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    else:
        state = State(**request.get_json())
        state.save()
        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updatestate(state_id=None):
    """updates a state"""
    obj = storage.get("State", state_id)
    if obj is None:
        abort(404)

    s = request.get_json(silent=True)
    if s is None:
        abort(400, "Not a JSON")
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
        obj.save()
        return jsonify(obj.to_dict), 200
