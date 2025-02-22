# from elasticsearch import Elasticsearch
# import os
# import json
# import logging
# from confluent_kafka import Consumer, KafkaError

# # Configure logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# # Environment variables
# ES_HOST = os.getenv("ELASTIC_HOST", "localhost")
# ES_PORT = int(os.getenv("ELASTIC_PORT", "9200"))
# ES_INDEX = os.getenv("ES_INDEX", "posts")
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
# LIKE_EVENTS_TOPIC = os.getenv("LIKE_EVENTS_TOPIC", "like_events")
# GROUP_ID = os.getenv("KAFKA_GROUP_ID", "post_ingestion_group")

# # Initialize Elasticsearch client
# es_client = Elasticsearch([{
#     'host': ES_HOST,
#     'port': ES_PORT,
#     'scheme': 'http'
# }])
# if not es_client.indices.exists(index=ES_INDEX):
#     # mapping = {
#     #     "mappings": {
#     #         "properties": {
#     #             "created_at": {"type": "date"},
#     #             "like_count": {"type": "integer"},
#     #             "content": {"type": "text"}
#     #         }
#     #     }
#     # }
#     # es_client.indices.create(index=ES_INDEX, body=mapping)
#     es_client.indices.create(index=ES_INDEX)

# def ingest_like_event(event):
#     """
#     Process a 'like' event and update Elasticsearch with the new like count.

#     Expected event format:
#     {
#       "type": "post_liked",
#       "data": {
#           "post_id": "some_id",
#           "like_count": 42
#       }
#     }
#     """
#     print("Ingesting like event into Elasticsearch:", event)

#     # Import the Elasticsearch client from your elastic_client module.
#     # Adjust the import path as necessary.

#     # Extract event data
#     data = event.get("data", {})
#     post_id = data.get("post_id")
#     like_count = data.get("like_count")

#     if post_id is None or like_count is None:
#         print("Invalid event data: 'post_id' or 'like_count' is missing.")
#         return

#     try:
#         # Update the like count in Elasticsearch for the given post
#         es_client.update_like_count(post_id, like_count)
#         print(f"Successfully updated post {post_id} with like count {like_count}.")
#     except Exception as e:
#         print(f"Error updating Elasticsearch for post {post_id}: {e}")

# def run_ingestion_worker():
#     """
#     Runs a Kafka consumer that listens for post events and processes them.
#     """
#     consumer_conf = {
#         'bootstrap.servers': KAFKA_BROKER,
#         'group.id': GROUP_ID,
#         'auto.offset.reset': 'earliest'
#     }
#     consumer = Consumer(consumer_conf)
#     consumer.subscribe([LIKE_EVENTS_TOPIC])
#     logging.info("Started ingestion worker, listening to Kafka topic '%s'", LIKE_EVENTS_TOPIC)
    
#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 continue
#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     continue
#                 else:
#                     logging.error("Kafka error: %s", msg.error())
#                     continue

#             try:
#                 event = json.loads(msg.value().decode('utf-8'))
#                 ingest_like_event(event)
#             except json.JSONDecodeError as e:
#                 logging.error("JSON decode error: %s", e)
#     except KeyboardInterrupt:
#         logging.info("Ingestion worker interrupted, shutting down.")
#     finally:
#         consumer.close()


from elasticsearch import Elasticsearch
import os
import json
import logging
from confluent_kafka import Consumer, KafkaError

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
    es_client.indices.create(index=ES_INDEX)
def ingest_like_event(event):
    """
    Process a 'like' event and increment the like_count in Elasticsearch by 1.
    
    Expected event format:
    {
      "type": "post_liked",
      "data": {
          "post_id": "some_id"
      }
    }
    Note: We no longer rely on the event providing the new like count;
          instead, we increment the existing count by 1.
    """
    print("Ingesting like event into Elasticsearch:", event)
    
    # Extract event data
    data = event.get("data", {})
    post_id = data.get("post_id")
    
    if post_id is None:
        print("Invalid event data: 'post_id' is missing.")
        return

    try:
        # Use a scripted update to increment like_count by 1
        es_client.update(
            index=ES_INDEX,
            id=post_id,
            body={
                "script": {
                    "source": """
                        if (ctx._source.like_count == null) {
                            ctx._source.like_count = params.increment;
                        } else {
                            ctx._source.like_count += params.increment;
                        }
                    """,
                    "lang": "painless",
                    "params": {"increment": 1}
                }
            }
        )
        print(f"Successfully incremented like count for post {post_id} by 1.")
    except Exception as e:
        print(f"Error updating Elasticsearch for post {post_id}: {e}")

# def ingest_like_event(event):
#     """
#     Process a 'like' event and update Elasticsearch with the new like count.
#     Expected event format:
#     {
#       "type": "post_liked",
#       "data": {
#           "post_id": "some_id",
#           "like_count": 42
#       }
#     }
#     """
#     print("Ingesting like event into Elasticsearch:", event)

#     # Extract event data
#     data = event.get("data", {})
#     post_id = data.get("post_id")
#     like_count = data.get("like_count")

#     if post_id is None or like_count is None:
#         print("Invalid event data: 'post_id' or 'like_count' is missing.")
#         return

#     try:
#         # Update the like count in Elasticsearch for the given post using the native update method
#         es_client.update(
#             index=ES_INDEX,
#             id=post_id,
#             body={"doc": {"like_count": like_count}}
#         )
#         print(f"Successfully updated post {post_id} with like count {like_count}.")
#     except Exception as e:
#         print(f"Error updating Elasticsearch for post {post_id}: {e}")

def run_ingestion_worker():
    """
    Runs a Kafka consumer that listens for like events and processes them.
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
                ingest_like_event(event)
            except json.JSONDecodeError as e:
                logging.error("JSON decode error: %s", e)
    except KeyboardInterrupt:
        logging.info("Ingestion worker interrupted, shutting down.")
    finally:
        consumer.close()
