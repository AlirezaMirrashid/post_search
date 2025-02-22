import os

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "localhost")
ELASTIC_PORT = os.getenv("ELASTIC_PORT", "9200")
ES_INDEX = os.getenv("ES_INDEX", "posts")
