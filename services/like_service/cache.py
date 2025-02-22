
import os, json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def cache_like(post_id, post):
    key = f"post:{post_id}"

    # Check if the post exists in cache
    cached_post = redis_client.get(key)

    if cached_post:
        # Post is in cache, update its like count
        post_data = json.loads(cached_post)
        post_data["like_count"] += 1
    else:
        # Post not in cache, fetch from DB
        if not post:
            return {"error": "Post not found"}, 404

        # Prepare post data
        post_data = {
            "id": post.id,
            "content": post.content,
            "created_at": post.created_at.isoformat(),
            "like_count": post.like_count + 1  # Increment the like count
        }

    # Cache the updated post with a TTL (1 hour)
    redis_client.set(key, json.dumps(post_data), ex=3600)