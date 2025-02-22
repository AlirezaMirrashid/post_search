# # In production, the API gateway might handle routing, authentication, etc.
# # For this simulation, assume that search_service/app.py acts as the gateway.
# def gateway_request(request):
    # # This function would parse and route requests appropriately.
    # pass
from flask import request, jsonify
import logging
from elastic_client import ElasticClient

def gateway_request(request):
    """
    Example API gateway request handler.
    This function:
      1. Checks for an Authorization header and validates the token.
      2. Routes the request based on the path.
         For this example, it only handles search requests.
    """
    # 1. Authenticate Request
    auth_header = request.headers.get("Authorization")
    if not auth_header or not validate_token(auth_header):
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Route Request
    if request.path.startswith("/search"):
        return route_search_request(request)
    else:
        # Could add more routing logic here for other endpoints.
        return jsonify({"error": "Endpoint not found"}), 404

def validate_token(token):
    """
    Dummy token validation.
    In production, use JWT or OAuth2 libraries to validate tokens.
    Expected token: "Bearer secret_token"
    """
    expected_token = "Bearer secret_token"
    return token == expected_token

def route_search_request(request):
    """
    Extracts search parameters from the request and calls the Elasticsearch client.
    """
    keyword = request.args.get("keyword", "")
    sort_by = request.args.get("sort_by", "recency")
    try:
        es_client = ElasticClient()
        results = es_client.search(keyword, sort_by)
        return jsonify(results), 200
    except Exception as e:
        logging.exception("Error processing search request")
        return jsonify({"error": "Internal server error"}), 500
