
from flask import Blueprint, request, jsonify
from elastic_client import ElasticClient
import logging

search_routes = Blueprint('search_routes', __name__)
es_client = ElasticClient()

@search_routes.route("/", methods=["GET"])
def search_posts():
    keyword = request.args.get("keyword", "")
    sort_by = request.args.get("sort_by", "recency")  # "recency" or "likes"
    search_type = request.args.get("search_type", "match")  # e.g., match, phrase, fuzzy, wildcard, regexp
    try:
        results = es_client.search(keyword, sort_by, search_type)
        return jsonify(results), 200
    except Exception as e:
        logging.exception("Error in search")
        return jsonify({"error": "Internal server error"}), 500
