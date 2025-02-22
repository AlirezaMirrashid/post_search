# from flask import Flask, request, jsonify
# import logging
# import requests  # To make HTTP requests to other services
# import os

# app = Flask(__name__)

# # Service URLs (using service names for Docker DNS resolution)
# # API_GATEWAY_URL = os.getenv("API_GATEWAY_URL",
# #                             "http://api_gateway:3000")  # Assuming the API Gateway is running at this URL
# POST_SERVICE_URL = os.getenv("POST_SERVICE_URL", "http://post_service:5001/posts/")
# LIKE_SERVICE_URL = os.getenv("LIKE_SERVICE_URL", "http://like_service:5002/likes/")
# SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL", "http://search_service:5003/search/")


# @app.route('/search', methods=['GET'])
# def search():
#     return route_search_request(request)

# @app.route('/like_post', methods=['POST'])
# def like_post():
#     return route_like_request(request)

# @app.route('/create_post', methods=['POST'])
# def create_post():
#     return route_post_request(request)


# def gateway_request(request):
#     """
#     Example API gateway request handler.
#     This function:
#       1. Checks for an Authorization header and validates the token.
#       2. Routes the request based on the path.
#     """
#     # 1. Authenticate Request
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not validate_token(auth_header):
#         return jsonify({"error": "Unauthorized"}), 401

#     # 2. Route Request
#     if request.path.startswith("/search"):
#         return route_search_request(request)
#     elif request.path.startswith("/like"):
#         return route_like_request(request)
#     elif request.path.startswith("/post"):
#         return route_post_request(request)
#     else:
#         return jsonify({"error": "Endpoint not found"}), 404


# def validate_token(token):
#     """
#     Dummy token validation.
#     In production, use JWT or OAuth2 libraries to validate tokens.
#     Expected token: "Bearer secret_token"
#     """
#     expected_token = "Bearer secret_token"
#     return token == expected_token


# def route_search_request(request):
#     """
#     Routes the search request to the search service via the API Gateway.
#     """
#     keyword = request.args.get("keyword", "")
#     sort_by = request.args.get("sort_by", "recency")
#     search_type = request.args.get("search_type", "match")

#     if not keyword:
#         return jsonify({"error": "keyword is required"}), 400

#     # Instead of calling the API Gateway itself, call the Search Service directly
#     search_service_url = f"http://search_service:5003/search"  # Directly call the Search Service

#     try:
#         # Forward the request to the Search Service
#         response = requests.get(search_service_url, params={
#             "keyword": keyword,
#             "sort_by": sort_by,
#             "search_type": search_type
#         })
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         logging.exception("Error calling search service")
#         return jsonify({"error": "Internal server error"}), 500


# def route_like_request(request):
#     """
#     Routes the like request to the like service.
#     """
#     post_id = request.args.get("post_id")
#     if not post_id:
#         return jsonify({"error": "Post ID is required"}), 400

#     # Assuming like_service is running on port 5002
#     like_service_url = f"http://like_service:5002/like/{post_id}"
#     try:
#         response = requests.post(like_service_url)
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         logging.exception("Error calling like service")
#         return jsonify({"error": "Internal server error"}), 500


# def route_post_request(request):
#     """
#     Routes the post request to the post service.
#     """
#     post_id = request.args.get("post_id")
#     if not post_id:
#         return jsonify({"error": "Post ID is required"}), 400

#     # Assuming post_service is running on port 5001
#     post_service_url = f"http://post_service:5001/post/{post_id}"
#     try:
#         response = requests.get(post_service_url)
#         return jsonify(response.json()), response.status_code
#     except requests.exceptions.RequestException as e:
#         logging.exception("Error calling post service")
#         return jsonify({"error": "Internal server error"}), 500

# if __name__ == '__main__':
#     app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))


import os
import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Service base URLs (Docker DNS resolution)
POST_SERVICE_URL = os.getenv("POST_SERVICE_URL", "http://post_service:5001/posts/").rstrip("/")
LIKE_SERVICE_URL = os.getenv("LIKE_SERVICE_URL", "http://like_service:5002/likes/").rstrip("/")
SEARCH_SERVICE_URL = os.getenv("SEARCH_SERVICE_URL", "http://search_service:5003/search/").rstrip("/")


def validate_token(token):
    """
    Dummy token validation.
    In production, use a proper method (e.g. JWT, OAuth2).
    Expected token format: "Bearer secret_token"
    """
    expected_token = "Bearer secret_token"
    return token == expected_token


def require_auth(func):
    """
    Decorator to require an Authorization header.
    """
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not validate_token(auth):
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/search', methods=['GET'])
@require_auth
def search():
    # Extract query parameters
    keyword = request.args.get("keyword", "")
    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400
    sort_by = request.args.get("sort_by", "recency")
    search_type = request.args.get("search_type", "match")

    try:
        # Forward the search request to the Search Service
        resp = requests.get(f"{SEARCH_SERVICE_URL}", params={
            "keyword": keyword,
            "sort_by": sort_by,
            "search_type": search_type
        })
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        logging.exception("Error calling search service")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/create_post', methods=['POST'])
@require_auth
def create_post():
    data = request.get_json()
    if not data or "content" not in data:
        return jsonify({"error": "Content is required"}), 400

    try:
        # Forward the post creation request to the Post Service
        resp = requests.post(f"{POST_SERVICE_URL}", json=data)
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        logging.exception("Error calling post service")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/like_post', methods=['POST'])
@require_auth
def like_post():
    data = request.get_json()
    if not data or "post_id" not in data:
        return jsonify({"error": "Post ID is required"}), 400

    post_id = data["post_id"]
    try:
        # Forward the like request to the Like Service
        # like_service_url = f"{LIKE_SERVICE_URL}/like/"
        resp = requests.post(f"{LIKE_SERVICE_URL}", json={"post_id": post_id})
        # resp = requests.post(f"{LIKE_SERVICE_URL}/{post_id}")
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        logging.exception("Error calling like service")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/post', methods=['GET'])
@require_auth
def get_post():
    post_id = request.args.get("post_id")
    if not post_id:
        return jsonify({"error": "Post ID is required"}), 400

    try:
        # Forward the get post request to the Post Service
        resp = requests.get(f"{POST_SERVICE_URL}/{post_id}")
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        logging.exception("Error calling post service")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
