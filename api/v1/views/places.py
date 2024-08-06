#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Place objects"""

from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """
    Retrieves a list of all Places obj of a City
    """
    city_d = storage.get(City, city_id)

    if not city_d:
        abort(404)

    all_places = [place.to_dict() for place in city_d.places]

    return jsonify(all_places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    retrieves a single Place obj using id
    """
    place_d = storage.get(Place, place_id)
    if not place_d:
        abort(404)

    return jsonify(place_d.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place obj
    """
    place_o = storage.get(Place, place_id)

    if not place_o:
        abort(404)

    storage.delete(place_o)
    storage.save()

    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place
    """
    city_o = storage.get(City, city_id)

    if not city_o:
        abort(404)

    data_city = request.get_json(silent=True)

    if not data_city:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in data_city:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data_city['user_id'])

    if not user:
        abort(404)

    if 'name' not in data_city:
        return jsonify({"error": "Missing name"}), 400

    data_city["city_id"] = city_id

    new_place_obj = Place(**data_city)
    new_place_obj.save()

    return jsonify(new_place_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def advanced_search():
    """
    Retrieves all Place objects that meet the optional
    filter passed in the body of the request as JSON
    - states: list of State ids
    - cities: list of City ids
    - amenities: list of Amenity ids
    """

    # get posted data
    data = request.get_json()
    states = data.get("states", None)
    cities = data.get("cities", None)
    amenities = data.get("amenities", None)

    # check posted data
    if data is None:
        abort(400, "Not a JSON")

    # none of the filters is provided
    if not data or all([not states, not cities, not amenities]):
        all_places = [place.to_dict() for place in storage.all(Place).values()]
        return jsonify(all_places)

    # list holds result after applying filters
    places_list = []

    if states:
        states_list = [storage.get(State, id) for id in states]
        for state in states_list:
            # check state it could be None!
            if state:
                for city in state.cities:
                    for place in city.places:
                        places_list.append(place)

    if cities:
        cities_list = [storage.get(City, id) for id in cities]
        for city in cities_list:
            # check city it could be None!
            if city:
                for place in city.places:
                    # avoid duplicates
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_list = [storage.get(Amenity, id) for id in amenities]
        temp_list = []
        for place in places_list:
            for amenity in amenities_list:
                if amenity in place.amenities:
                    temp_list.append(place)

        places_list = temp_list

    # prepare places list
    places = [place.to_dict() for place in places_list]
    # remove amenities key from each place dictionary
    [place.pop("amenities", None) for place in places if "amenities" in place]

    return jsonify(places)
