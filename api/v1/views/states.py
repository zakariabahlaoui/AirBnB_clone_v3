#!/usr/bin/python3
"""handles all default RESTFul API actions for State objects"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    '''
        Retrieves the list of all State objects
    '''
    states_dict = storage.all(State)
    return jsonify([objct.to_dict() for objct in states_dict.values()])

@app_views.route("/states/<string:state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    '''
        retrieve one State object
    '''
    state = storage.get(State, state_id)

    # check if state object exists
    if state is None:
        abort(404)

    return jsonify(state.to_dict())