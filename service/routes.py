"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, make_response, abort, url_for
from service.models import Account
from service.common import status
from . import app  # Import Flask application

HEADER_CONTENT_TYPE = "application/json"

############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )

######################################################################
# CREATE A NEW ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates an Account"""
    app.logger.info("Request to create an Account")
    check_content_type(HEADER_CONTENT_TYPE)
    account = Account()
    account.deserialize(request.get_json())
    account.create()
    message = account.serialize()
    location_url = url_for("read_account", account_id=account.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED, {"Location": location_url})

######################################################################
# LIST ALL ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_all_accounts():
    """List all accounts"""
    app.logger.info("Request to list all accounts")
    account_list = Account.all()
    app.logger.info("[%s] accounts found.", len(account_list))
    message = [account.serialize() for account in account_list]
    return jsonify(message), status.HTTP_200_OK

######################################################################
# READ AN ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id: int):
    """Read an account by ID"""
    app.logger.info("Request to read an account")
    account = Account.find(account_id)
    if account is None:
        app.logger.info("No account with ID %s found.", account_id)
        abort(status.HTTP_404_NOT_FOUND, f"Account with id '{account_id}' was not found.")
    return jsonify(account.serialize()), status.HTTP_200_OK

######################################################################
# UPDATE AN EXISTING ACCOUNT