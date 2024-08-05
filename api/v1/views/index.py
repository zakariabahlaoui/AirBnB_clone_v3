#!/usr/bin/python3
"""This module contains functions for endpoint routes to get the status of
my API and retrieve counts of different objects.
"""

from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """Endpoint that returns the status of the API.

    Returns:
        A JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_each_obj():
    """Endpoint that retrieves the number of each object by type.

    Returns:
        A JSON response with counts of various object types.
    """
    obj_counter = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(obj_counter)
