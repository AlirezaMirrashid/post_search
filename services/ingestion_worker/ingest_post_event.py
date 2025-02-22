import os
import json
import logging
from confluent_kafka import Consumer, KafkaError
from elasticsearch import Elasticsearch

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", "9200"))
ES_INDEX = os.getenv("ES_INDEX", "posts")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
POST_EVENTS_TOPIC = os.getenv("POST_EVENTS_TOPIC", "post_events")
GROUP_ID = os.getenv("KAFKA_GROUP_ID", "post_ingestion_group")

es_client = Elasticsearch([{
    'host': ELASTIC_HOST,
    'port': ELASTIC_PORT,
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
    try:
        if event.get("type") == "post_created":
            post = event.get("data")
            if not post or "id" not in post:
                logging.error("Invalid post data in event: %s", event)
                return
            response = es_client.index(index=ES_INDEX, id=post["id"], body=post)
            logging.info("Indexed post %s: %s", post["id"], response)
        elif event.get("type") == "post_liked":
            data = event.get("data")
            post_id = data.get("post_id")
            like_count = data.get("like_count")
            response = es_client.update(
                index=ES_INDEX,
                id=post_id,
                body={"doc": {"like_count": like_count}}
            )
            logging.info("Updated like count for post %s: %s", post_id, response)
        else:
            logging.warning("Unsupported event type: %s", event.get("type"))
    except Exception as e:
        logging.exception("Error ingesting event: %s", e)

def run_ingestion_worker():
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
