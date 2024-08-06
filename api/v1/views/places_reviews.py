#!/usr/bin/python3
"""
Reviews web route
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews(place_id):
    """Retrieve a place reviews"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(place_id):
    """
    retrieves list of all Review obj place
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    p_reviews = [review.to_dict() for review in place.reviews]

    return jsonify(p_reviews)


@app_views.route(
        '/reviews/<review_id>',
        methods=["DELETE"],
        strict_slashes=False
    )
def delete_review(review_id):
    """Deletes a review"""
    p_review = storage.get(Review, review_id)

    if not p_review:
        abort(404)

    storage.delete(p_review)
    storage.save()

    return jsonify({})


@app_views.route(
        '/places/<place_id>/reviews',
        methods=["POST"],
        strict_slashes=False
    )
def create_review(place_id):
    """Creates a new review for a place"""
    place_d = storage.get(Place, place_id)

    if not place_d:
        abort(404)

    data_p = request.get_json(silent=True)

    if not data_p:
        return jsonify({"error": "Not a JSON"}), 400

    if 'user_id' not in data_p:
        return jsonify({"error": "Missing user_id"}), 400

    if not storage.get(User, data_p['user_id']):
        abort(404)

    if 'text' not in data_p:
        return jsonify({"error": "Missing text"}), 400

    data_p['place_id'] = place_id

    new_review_p = Review(**data_p)
    new_review_p.save()

    return jsonify(new_review_p.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=["PUT"],
        strict_slashes=False
    )
def put_review(review_id):
    """
    updates a Review
    """
    review_p = storage.get(Review, review_id)

    if not review_p:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_key = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore_key:
            setattr(review_p, key, value)
    storage.save()
    return make_response(jsonify(review_p.to_dict()), 200)
