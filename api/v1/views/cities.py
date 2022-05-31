#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Cities' """
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def getAllCities(state_id):
    """Returns the list of all Cities of a State"""
    # Retireve the state from storage using state_id
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return (jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getCity(city_id):
    """Returns a Cities object using the id"""
    # Retireve the city from storage using city_id
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deleteCity(city_id):
    """Deletes a City using its id"""
    # Retireve the city from storage using city_id
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def postCity(state_id):
    """Creates a new City in a given state using the state id"""
    # Retireve the state from storage using state_id
    state = storage.get('State', state_id)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    if dict is None:
        abort(400, "Not a JSON")
    elif "name" not in dict.keys():
        abort(400, "Missing name")
    else:
        dict['state_id'] = state.id
        new_city = City(**dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def putCity(city_id):
    """Updates a City object"""
    # Retireve the city from storage using city_id
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    else:
        for key, val in dict.items():
            if key in ['id', 'state_id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(city, key, val)
        storage.save()
        updatedCity = city.to_dict()
        return jsonify(updatedCity), 200
