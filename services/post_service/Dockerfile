# Use official Python image
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

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5001

# Run the Flask application
CMD ["python", "app.py"]
