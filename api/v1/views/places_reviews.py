#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Amenities' """
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage, amenity
from models.amenity import Amenity

