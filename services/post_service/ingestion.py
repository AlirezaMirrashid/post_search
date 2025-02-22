# # # In production, a background worker would listen for Kafka events and then
# # # index new posts into Elasticsearch.
# # def ingest_post_event(event):
    # # # Here we simply simulate ingestion.
    # # print("[Post Service] Ingesting post event into Elasticsearch:", event)
# def ingest_post_event(event):
    # # In production, implement a background worker that consumes Kafka events
    # # and uses an official Elasticsearch client to index the post.
    # print("Ingesting post event into Elasticsearch:", event)
import os
import json
import logging
from confluent_kafka import Consumer, KafkaError
from elasticsearch import Elasticsearch

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# Environment variables
ES_HOST = os.getenv("ELASTIC_HOST", "localhost")
ES_PORT = int(os.getenv("ELASTIC_PORT", "9200"))
ES_INDEX = os.getenv("ES_INDEX", "posts")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
POST_EVENTS_TOPIC = os.getenv("POST_EVENTS_TOPIC", "post_events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "post_ingestion_group")

# Initialize Elasticsearch client
es_client = Elasticsearch([{
    'host': ES_HOST,
    'port': ES_PORT,
    'scheme': 'http'
}])
if not es_client.indices.exists(index=ES_INDEX):
    # mapping = {
    #     "mappings": {
    #         "properties": {
    #             "created_at": {"type": "date"},
    #             "like_count": {"type": "integer"},
    #             "content": {"type": "text"}
    #         }
    #     }
    # }
    # es_client.indices.create(index=ES_INDEX, body=mapping)
    es_client.indices.create(index=ES_INDEX)

def ingest_post_event(event):
    """
    Processes a Kafka event containing a new post and indexes it into Elasticsearch.
    Expects an event dict in the following format:
    
    {
        "type": "post_created",
        "data": {
            "id": "post-id",
            "content": "post content",
            "created_at": 1621234567.89,
            "like_count": 0
        }
    }
    """
    try:
        if event.get("type") == "post_created":
            post = event.get("data")
            if not post or "id" not in post:
                logging.error("Invalid post data in event: %s", event)
                return

            # Index the post in Elasticsearch (upsert semantics)
            print(ES_INDEX, post["id"], post)
            response = es_client.index(index=ES_INDEX, id=post["id"], body=post)
            logging.info("Indexed post %s: %s", post["id"], response)
        else:
            logging.warning("Received unsupported event type: %s", event.get("type"))
    except Exception as e:
        logging.exception("Error ingesting post event: %s", e)

def run_ingestion_worker():
    """
    Runs a Kafka consumer that listens for post events and processes them.
    """
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([POST_EVENTS_TOPIC])
    logging.info("Started ingestion worker, listening to Kafka topic '%s'", POST_EVENTS_TOPIC)
    
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error("Kafka error: %s", msg.error())
                    continue

            try:
                event = json.loads(msg.value().decode('utf-8'))
                ingest_post_event(event)
            except json.JSONDecodeError as e:
                logging.error("JSON decode error: %s", e)
    except KeyboardInterrupt:
        logging.info("Ingestion worker interrupted, shutting down.")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_ingestion_worker()
