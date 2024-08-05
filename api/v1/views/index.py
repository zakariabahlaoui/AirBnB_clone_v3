#!/usr/bin/python3
"""Module to handle API routes related to object counts and status."""

from flask import Blueprint, jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review

app_views = Blueprint('app_views', __name__)


@app_views.route('/status')
def api_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_each_obj():
    """Retrieves the number of each object by type.

    Returns:
        JSON response with the count of each object type.
    """
    obj_counter = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    dic = {k: storage.count(v) for k, v in obj_counter.items()}

    return jsonify(dic)
