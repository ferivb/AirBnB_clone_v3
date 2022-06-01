#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Amenities' """
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage, place
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def getAllPlaces(city_id):
    """Returns a list of all Places"""
    if city_id is None:
        abort(404)
    places = []
    for place in storage.all("Place").values():
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def getPlace(place_id):
    """Returns a Place using its id"""
    # Retireve the place from storage using place_id
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    """Deletes a Place using its id"""
    # Retireve the place from storage using place_id
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def postPlace(city_id):
    """Creates a new Place"""
    # Retireve the city from storage using city_id
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    if dict is None:
        abort(400, "Not a JSON")
    if 'user_id' not in dict:
        abort(400, 'Missing user_id')
    if not storage.get(User, dict['user_id']):
        abort(404)
    if "name" not in dict.keys():
        abort(404, 'Missing name')

    dict["city_id"] = city_id
    place = Place(**dict)
    storage.new(place)
    storage.save
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def putPlace(place_id):
    """Updates a Place object"""
    # Retireve the aplace from storage using place_id
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    else:
        for key, val in dict.items():
            if key in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
                pass
            else:
                setattr(place, key, val)
        storage.save()
        updatedPlace = place.to_dict()
        return jsonify(updatedPlace), 200
