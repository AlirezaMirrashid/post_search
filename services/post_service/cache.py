
import os, json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def cache_post(post):
    key = f"post:{post.id}"
    value = json.dumps({
        "id": post.id,
        "content": post.content,
        "created_at": post.created_at,
        "like_count": post.like_count
    })
    # Cache with a TTL (e.g. 1 hour)
    redis_client.set(key, value, ex=3600)
