#!/usr/bin/python3
""" API main file """

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ method to handle teardown of database"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Returns JSON error repsponse"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True, debug=True)
