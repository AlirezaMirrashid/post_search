
from kafka_producer import KafkaProducer
import json

def write_like_event(post_id, like_count):
    event = {
        "type": "post_liked",
        "data": {
            "post_id": post_id,
            "like_count": like_count
        }
    }
    producer = KafkaProducer()
    producer.publish("post_events", event)
