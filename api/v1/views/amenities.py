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


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def getAmenity(amenity_id):
    """ Returns an Amenity using its id"""
    # Retireve the state from storage using state_id
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteAmenity(amenity_id):
    """ Deletes an Amenity using its id"""
    # Retireve the state from storage using state_id
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def postAmenity():
    """Creates a new Amenity"""
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    elif "name" not in dict.keys():
        abort(400, "Missing name")
    else:
        new_amenity = amenities.Amenity(**dict)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def putAmenity(state_id=None):
    """Updates an Amenity object"""
    # Retireve the amenity from storage using amenity_id
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
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
                setattr(amenity, key, val)
        storage.save()
        updatedAmenity = amenity.to_dict()
        return jsonify(updatedAmenity), 200
