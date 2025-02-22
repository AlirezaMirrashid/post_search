# Post Search

A microservices-based application simulating a social media platform for creating, liking, and searching posts. This project demonstrates the integration of several services using Docker, Flask, PostgreSQL, Redis, Kafka, Elasticsearch, and more.

## Project Overview

The application is composed of several services:

- **API Gateway:** Routes requests from the UI to the appropriate backend services.
- **Post Service:** Manages the creation and retrieval of posts.
- **Like Service:** Handles post likes.
- **Search Service:** Provides search functionality for posts.
- **UI Service:** A simple Flask web interface for interacting with the system.
- **Ingestion Worker:** Processes events (e.g., new posts) for indexing.
- **Supporting Services:** PostgreSQL (data persistence), Redis (caching), Kafka & Zookeeper (messaging), Elasticsearch (search).

## Architecture

The services communicate over Docker networks using service names. The API Gateway acts as the central entry point, forwarding requests to the Post, Like, and Search services.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/)

## Getting Started

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/facebook_post_search.git
   cd facebook_post_search
Build and Run All Services:

Use Docker Compose to build and run the entire stack:

bash
Copy
Edit
docker-compose up --build
This command starts the following services:

PostgreSQL
Redis
Zookeeper
Kafka
Elasticsearch
Post Service
Like Service
Search Service
API Gateway
UI Service
Ingestion Worker
Access the Application:

UI: Open http://localhost:5000 in your browser.
API Gateway: Accessible at http://localhost:3000 (for API testing).
API Endpoints
API Gateway
POST /create_post
Create a new post by forwarding the request to the Post Service.

POST /like_post
Like a post by forwarding the request to the Like Service.

GET /search
Search posts by forwarding the query to the Search Service.

GET /post?post_id=<id>
Retrieve a specific post from the Post Service.

Post Service
POST /posts
Create a new post.
Example Request Body:

json
Copy
Edit
{
  "content": "Hello, world!"
}
GET /posts
Retrieve all posts.

Like Service
POST /like
Like a post.
Example Request Body:
json
Copy
Edit
{
  "post_id": "your-post-id"
}
Search Service
GET /search
Search posts by keyword.
Example Query Parameters:
?keyword=hello&sort_by=recency&search_type=match
Environment Variables
The services use the following environment variables (set in the docker-compose.yml):

POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB: For PostgreSQL configuration.
REDIS_HOST, REDIS_PORT: For Redis.
KAFKA_BROKER, ZOOKEEPER_CONNECT: For Kafka messaging.
ELASTIC_HOST, ELASTIC_PORT, ES_INDEX: For Elasticsearch.
API_GATEWAY_URL: Used by the UI to connect to the API Gateway.
Troubleshooting
Dependency Hash Mismatch:
If you encounter errors related to package hashes (e.g., for SQLAlchemy), update or remove the hash values in your requirements.txt.

Service Connectivity Issues:
Ensure that service names in the Docker Compose file match those used in the code (e.g., post_service, like_service, search_service).

Logs:
Check logs with:

bash
Copy
Edit
docker-compose logs <service_name>
For example:

bash
Copy
Edit
docker-compose logs api_gateway
Contributing
Contributions are welcome! Please submit issues and pull requests to help improve the project.

License
This project is licensed under the MIT License. See the LICENSE file for details.
