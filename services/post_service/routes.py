

from flask import Blueprint, request, jsonify
from models import Post
from database import SessionLocal
from event_writer import write_post_created_event
from cache import cache_post
import logging

post_routes = Blueprint('post_routes', __name__)

@post_routes.route("/", methods=["POST"])
def create_post():
    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "Content required"}), 400

    session = SessionLocal()
    try:
        new_post = Post(content=content)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)

        # Cache the post in Redis
        cache_post(new_post)
        # Publish an event to Kafka so that Search Service can index the new post.
        write_post_created_event(new_post)
        return jsonify({
            "id": new_post.id,
            "content": new_post.content,
            "created_at": new_post.created_at,
            "like_count": new_post.like_count
        }), 201
    except Exception as e:
        session.rollback()
        logging.exception("Error creating post")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()

@post_routes.route("/", methods=["GET"])
def get_all_posts():
    session = SessionLocal()
    try:
        posts = session.query(Post).all()
        results = [{
            "id": post.id,
            "content": post.content,
            "created_at": post.created_at,
            "like_count": post.like_count
        } for post in posts]
        return jsonify(results), 200
    except Exception as e:
        logging.exception("Error fetching posts")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()
