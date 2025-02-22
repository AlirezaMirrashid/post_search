
import os
from elasticsearch import Elasticsearch

ELASTIC_HOST = os.getenv("ELASTIC_HOST", "elasticsearch")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", "9200"))  # Convert to int

ES_INDEX = os.getenv("ES_INDEX", "posts")

class ElasticClient:
    def __init__(self):
        self.client = Elasticsearch([{
                    'host': ELASTIC_HOST,
                    'port': ELASTIC_PORT,
                    'scheme': 'http'
                    }])
        # Ensure the index exists.
        if not self.client.indices.exists(index=ES_INDEX):
            # mapping = {
            #     "mappings": {
            #         "properties": {
            #             "created_at": {"type": "date"},
            #             "like_count": {"type": "integer"},
            #             "content": {"type": "text"}
            #         }
            #     }
            # }
            # self.client.indices.create(index=ES_INDEX, body=mapping)
            self.client.indices.create(index=ES_INDEX)

    def index_post(self, post):
        self.client.index(index=ES_INDEX, id=post["id"], body=post)

    def update_like_count(self, post_id, like_count):
        self.client.update(
            index=ES_INDEX,
            id=post_id,
            body={"doc": {"like_count": like_count}}
        )

    def search(self, keyword, sort_by="recency", search_type="match"):
        """
        Search for posts with a given keyword using different search types.
        
        :param keyword: The search term.
        :param sort_by: Either "recency" or "likes".
        :param search_type: The type of search to perform. Options include:
            - "match": Standard full-text match.
            - "phrase": Exact phrase search.
            - "fuzzy": Fuzzy matching.
            - "wildcard": Wildcard query.
            - "regexp": Regular expression query.
        :return: A list of posts matching the search criteria.
        """
        # Define the query based on the search type.
        if search_type == "match":
            query_body = {
                "query": {
                    "match": {
                        "content": keyword
                    }
                }
            }
        elif search_type == "phrase":
            query_body = {
                "query": {
                    "match_phrase": {
                        "content": keyword
                    }
                }
            }
        elif search_type == "fuzzy":
            query_body = {
                "query": {
                    "fuzzy": {
                        "content": {
                            "value": keyword,
                            "fuzziness": "AUTO"
                        }
                    }
                }
            }
        elif search_type == "wildcard":
            query_body = {
                "query": {
                    "wildcard": {
                        "content": {
                            "value": f"*{keyword}*"
                        }
                    }
                }
            }
        elif search_type == "regexp":
            query_body = {
                "query": {
                    "regexp": {
                        "content": {
                            "value": keyword
                        }
                    }
                }
            }
        else:
            # Default to standard match query.
            query_body = {
                "query": {
                    "match": {
                        "content": keyword
                    }
                }
            }

        # Add sorting to the query.
        if sort_by == "recency":
            sort_clause = {"created_at": {"order": "desc", "unmapped_type" : "date"}}
        elif sort_by == "likes":
            sort_clause = {"like_count": {"order": "desc", "unmapped_type" : "integer"}}
        else:
            sort_clause = {"created_at": {"order": "desc", "unmapped_type" : "date"}}

        query_body["sort"] = [sort_clause]
        # print(ES_INDEX, query_body)
        response = self.client.search(index=ES_INDEX, body=query_body)
        hits = response.get("hits", {}).get("hits", [])
        return [hit["_source"] for hit in hits]

