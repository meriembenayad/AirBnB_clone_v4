#!/usr/bin/python3
"""
Create Flask app; and register the blueprint app_views to Flask instance app.
"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)


# enable CORS and allow for origins:
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Register the app_views blueprint:
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


# Teardown function to close the SQLAlchemy Session object after each request:
@app.teardown_appcontext
def teardown_engine(exception):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()

# Task 5: Error handlers for expected app behavior:


@app.errorhandler(404)
def not_found(error):
    """
    Return errmsg `Not Found`.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
