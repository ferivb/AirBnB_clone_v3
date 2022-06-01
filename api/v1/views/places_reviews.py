#!/usr/bin/python3
"""Handles all RESTful API verbs for class 'Reviews' """


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage, review
from models.review import Review
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def getAllReviews(place_id):
    """Returns the list of all Reviews of a place"""
    # Retireve the place from storage using place_id
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return (jsonify(reviews), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def getSingleReview(review_id=None):
    """Retrieves a Review object"""
    singleReview = storage.get("Review", review_id)
    if singleReview is None:
        abort(404)
    else:
        return jsonify(singleReview.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deleteReview(review_id=None):
    """Deletes a Review object"""
    singleReview = storage.get("Review", review_id)
    if singleReview is None:
        abort(404)
    else:
        storage.delete(singleReview)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def postReview(place_id):
    """Creates a new Review in a given Place using the place_id"""
    # Retireve the place from storage using state_id
    place = storage.get('Place', place_id)
    user = storage.all("User")
    if place is None:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    if dict is None:
        abort(400, "Not a JSON")
    elif "user_id" not in dict.keys():
        abort(400, "Missing user_id")
    # elif dict["user_id"] not in user.values():
    #     test = User.__str__(user)
    #     print(type(user))
    #     abort(400, f"{test}")
    elif "text" not in dict.keys():
        abort(400, "Missing text")
    else:
        dict['place_id'] = place.id
        new_review = Review(**dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def putReview(review_id=None):
    """Updates a Review object"""
    # Retireve the user from storage using user_id
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    # Parses the incoming JSON request data and returns it as a dict
    dict = request.get_json()
    # dict will == None if the mimetype is not application/json
    if dict is None:
        abort(400, "Not a JSON")
    else:
        for key, val in dict.items():
            if key in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
                pass
            else:
                setattr(review, key, val)
        storage.save()
        updatedReview = review.to_dict()
        return jsonify(updatedReview), 200
