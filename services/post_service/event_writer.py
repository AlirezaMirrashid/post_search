

from kafka_producer import KafkaProducer
import json

def write_post_created_event(post):
    event = {
        "type": "post_created",
        "data": {
            "id": post.id,
            "content": post.content,
            "created_at": post.created_at,
            "like_count": post.like_count
        }
    }
    producer = KafkaProducer()
    producer.publish("post_events", event)
