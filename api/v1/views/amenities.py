#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Amenities' """
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def getAllAmenities():
    """ Gets all the Amenities """
    amenitys = []
    for amenity in storage.all("Amenity").values():
        amenitys.append(amenity.to_dict())
    return jsonify(amenitys)
