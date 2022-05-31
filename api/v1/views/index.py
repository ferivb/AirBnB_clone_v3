#!/usr/bin/python3
"""Api connector index"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """Status of the server"""
    return jsonify({"status": "OK"})
