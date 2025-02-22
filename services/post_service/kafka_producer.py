
import os
import json
from confluent_kafka import Producer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")

class KafkaProducer:
    def __init__(self):
        conf = {'bootstrap.servers': KAFKA_BROKER}
        self.producer = Producer(conf)

    def publish(self, topic, event):
        try:
            self.producer.produce(topic, json.dumps(event))
            self.producer.flush()
        except Exception as e:
            # In production, use a proper logging framework.
            print(f"Error publishing to Kafka: {e}")
