
from flask import Blueprint, request, jsonify
from models import Post
from database import SessionLocal
from event_writer import write_like_event
from cache import cache_like
import logging

like_routes = Blueprint('like_routes', __name__)

@like_routes.route("/", methods=["POST"])
def like_post():
    data = request.get_json()
    post_id = data.get("post_id")
    if not post_id:
        return jsonify({"error": "post_id required"}), 400

    session = SessionLocal()
    try:
        post_obj = session.query(Post).filter_by(id=post_id).first()
        post_obj.like_count += 1
        session.add(post_obj)
        session.commit()

        # Update Redis cache
        cache_like(post_id, post_obj)
        # Publish like event to Kafka.
        write_like_event(post_id, post_obj.like_count)
        return jsonify({"post_id": post_id, "like_count": post_obj.like_count}), 200
    except Exception as e:
        session.rollback()
        logging.exception("Error liking post")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()

@like_routes.route("/", methods=["GET"])
def popular_posts():
    session = SessionLocal()
    try:
        likes = session.query(Post).order_by(Post.like_count.desc()).all()
        results = [{"post_id": like.post_id, "like_count": like.like_count} for like in likes]
        return jsonify(results), 200
    except Exception as e:
        logging.exception("Error fetching popular posts")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        session.close()
