"""
Routes for the Account Service
"""

from flask import Blueprint, jsonify, request, abort
from service.common import status
from service.models import Account

# Create the Blueprint for routes
api = Blueprint("api", __name__)

######################################################################
# INDEX
######################################################################
@api.route("/", methods=["GET"])
def index():
    """Returns a simple greeting message for the root URL"""
    return jsonify(name="Account REST API Service", version="1.0"), status.HTTP_200_OK


######################################################################
# HEALTH CHECK
######################################################################
@api.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(status="OK"), status.HTTP_200_OK


######################################################################
# INTERNAL SERVER ERROR (FOR TESTING)
######################################################################
@api.route("/boom", methods=["GET"])
def boom():
    """Endpoint to deliberately trigger a 500 Internal Server Error"""
    raise Exception("Boom!")  


######################################################################
# CREATE AN ACCOUNT
######################################################################
@api.route("/accounts", methods=["POST"])
def create_account():
    """Creates a new Account"""
    if not request.is_json:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    data = request.get_json()
    account = Account()
    account.deserialize(data)
    account.create()
    return jsonify(account.serialize()), status.HTTP_201_CREATED
