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
   ```
2. **Build and Run All Services:**
Use Docker Compose to build and run the entire stack:

   ```bash   
   docker-compose up --build
   ```
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

3. **Access the Application:**

   UI: Open http://localhost:5000 in your browser.
   API Gateway: Accessible at http://localhost:3000 (for API testing).
   
4. **License:**
This project is licensed under the MIT License. See the LICENSE file for details.
