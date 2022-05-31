#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Amenities' """
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage, place
from models.place import Place
from models.city import City

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
