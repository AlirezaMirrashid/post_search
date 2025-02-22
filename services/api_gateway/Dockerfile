FROM python:3.10

# Ensure Python outputs are unbuffered (good for logging in Docker)
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app


COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 3000

# Run the Flask application
CMD ["python", "api_gateway.py"]
