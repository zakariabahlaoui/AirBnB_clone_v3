#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Amenity objects"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """ Retrieves a list of all amenities """
    amenitie_data = storage.all(Amenity).values()
    list_amenities = [amenity.to_dict() for amenity in amenitie_data]

    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves an amenity  object """
    amenity_d = storage.get(Amenity, amenity_id)
    if not amenity_d:
        abort(404)

    return jsonify(amenity_d.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes amenity """
    amenity_d = storage.get(Amenity, amenity_id)

    if not amenity_d:
        abort(404)

    storage.delete(amenity_d)
    storage.save()

    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an amenity  obj"""
    amen_data = request.get_json(silent=True)
    if not amen_data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in amen_data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity_d = Amenity(**amen_data)
    new_amenity_d.save()
    return jsonify(new_amenity_d.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an amenity obj """
    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data_amenity = request.get_json()

    if not data_amenity:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data_amenity.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict())
