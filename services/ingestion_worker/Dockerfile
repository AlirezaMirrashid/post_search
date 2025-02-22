FROM python:3.10

# Ensure Python outputs are unbuffered (good for logging in Docker)
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Update package lists and install required system packages:
#   - librdkafka-dev: Provides librdkafka/rdkafka.h needed by confluent-kafka
#   - gcc: For compiling any C extensions
RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# No need to expose a port since it's a worker
CMD ["python", "ingest_post_event.py"]
